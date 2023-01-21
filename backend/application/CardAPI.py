from application.api import *
from application.models import User, List, Card
from datetime import date, datetime
import matplotlib
from application.helperfunction import *
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import math


card_fields = {
    'id':   fields.Integer,
    'title':    fields.String,
    'content':    fields.String,
    'created_time':     fields.DateTime,
    'completed':fields.Integer,
    'completed_time':fields.DateTime,
    'list_id':fields.Integer,
    'deadline':  fields.DateTime,
    'deadline_days':fields.Integer,
    
}
create_card_parser = reqparse.RequestParser()
create_card_parser.add_argument('title', required=True)
create_card_parser.add_argument('content',  required=True)
create_card_parser.add_argument('deadline',  required=True)

update_card_parser = reqparse.RequestParser()
update_card_parser.add_argument('title', required=True)
update_card_parser.add_argument('content',  required=True)
update_card_parser.add_argument('deadline',  required=True)
update_card_parser.add_argument('list_move_id',  required=True)
class CardAPI(Resource):
    @jwt_required()
    @marshal_with(card_fields)
    def get(self, list_id):
        list = List.query.filter_by(id=list_id).first()
        
        if not list:
            return {'status':False}
            
        cards = Card.query.filter_by(list_id=list_id).all()
        if len(cards)==0:
            return {'status':False}
        for card in cards:
            deadline = card.deadline
            
            date_today=datetime.today()
            deadline_days=(deadline-date_today).days
            if deadline_days != card.deadline_days:
                card.deadline_days = deadline_days
            
            # print(deadline_days)
            # deadlinestr=str(deadline_days+1)+'days left'
            # if deadline_days <-1:
            #     card.completed=2
            #     deadlinestr='Deadline passed'
            # elif deadline_days==-1:
            #     deadlinestr='Deadline is today'
            # elif deadline_days==0:
            #     deadlinestr='Deadline is tomorrow'
        db.session.commit()
        if len(cards)==0:
            raise BusinessValidationError(
                status_code=400, error_code="CARD001", error_message="No card created for the deck")
        else:
            return cards
        
    
    def put(self, card_id):
        card= Card.query.filter_by(id=card_id).first()
        if not card:
            return{'status':False,'error_message':'Card not found'},401
        list_id = card.list_id
        list = List.query.filter_by(id=list_id).first()
        args = update_card_parser.parse_args()
        title = args.get('title',None)
        content = args.get('content',None)
        deadline= args.get('deadline',None)
        list_move_id= args.get('list_move_id',None)
        # if front is None or len(front)==0:
        #     raise BusinessValidationError(
        #         status_code=400, error_code="CARD002", error_message="Front of the card should be non-empty")
        # if back is None or len(back)==0:
        #     raise BusinessValidationError(
        #         status_code=400, error_code="CARD003", error_message="Back of the card should be non-empty")
        # card_exist =Card.query.filter_by(front=front,back=back,deck_id=deck_id).first()
        # if card_exist:
        #     raise AlreadyExistedError(status_code=409)
        if card.title != title:
            card.title = title
        if card.content!= content:
            card.content = content
        card_deadline= card.deadline.date()
        year,month, day=map(int,deadline.split('-'))
        deadline_new=date(year, month, day)
        print(card.deadline != deadline_new)
        if card.deadline != deadline_new:
            card.deadline = deadline_new
            card.deadline_days=(deadline_new-date.today()).days
        if list_id != list_move_id:
            card.list_id = list_move_id
        card.updated_time=date.today()
        db.session.commit()
        return {'status':True}
        


    def delete(self,card_id):
        card= Card.query.filter_by(id=card_id).first()
        if not card:
            return{'status':False,'error_message':'Card not found'},401
        db.session.delete(card)
        db.session.commit()
        return {'status':True}

   
    def post(self, list_id):
        list = List.query.filter_by(id=list_id).first()
        if not list:
            return{'status':False,'error_message':'List not found'},401
        args = create_card_parser.parse_args()
        title = args.get('title',None)
        content = args.get('content',None)
        deadline= args.get('deadline',None)
        created_time=date.today()
        year,month, day=map(int,deadline.split('-'))
        deadline_new=date(year, month, day)
        deadline_days=(deadline_new-created_time).days
        card=Card(title=title, content=content, list_id=list_id,created_time=created_time,deadline=deadline_new,deadline_days=deadline_days)
        db.session.add(card)
        db.session.commit()
        return {'status':True,'msg':'Card Created'},200
api.add_resource(CardAPI,"/api/card/list/<int:list_id>",'/api/card/<int:card_id>')
class CardsAPI(Resource):
    
    @jwt_required()
    def get(self):
        current_user=get_jwt_identity()
        user = find_user(current_user)
        if not user:
            return jsonify({'msg':'No user with the username','status':False}),401
            
        lists = find_all_list(user.user_id)
        if len(lists)==0:
            return jsonify({'msg':'No list created for the user','status':False}),401
            
        all_lists=[]
        incomplete=0
        completed=0
        passed=0
        for list in lists:
            cards = Card.query.filter_by(list_id=list.id).all()
            list_cards=[]
            completed_time=""
            for card in cards:
                if card.completed==1:
                    completed_time=card.completed_time.strftime('%d-%m-%Y')
                    completed+=1
                elif (int(card.deadline_days)<-1):
                    passed+=1
                elif (int(card.deadline_days)>=-1):
                    incomplete+=1

                jsonified_card = {
        'title':    card.title,
        'content':    card.content,
        'list_title':list.title,
         'deadline':    card.deadline.strftime('%d-%m-%Y'),
          'completed':card.completed,
        'completed_time':completed_time,
        'deadline_days':card.deadline_days,
        }
                list_cards.append(jsonified_card)   
            
            all_lists+=list_cards
        
        image_labels=['To be completed','Completed', 'Deadline Passed']
        image_data=[incomplete,completed,passed]
        max_data=max(image_data)
        yint = range(max_data+1)

        buf=BytesIO()
        
        plt.bar(image_labels,image_data,color=['yellow','green','red'])
        plt.ylabel('No. of tasks')
        plt.yticks(yint)
        plt.savefig(buf,format='png')
        plt.close()
        buf.seek(0)
        image_base64=base64.b64encode(buf.getvalue()).decode()



        if len(all_lists)==0:
            return jsonify({'msg':'No card created for the user','status':False}),401
        else:
            return jsonify({'all_lists':all_lists,'msg':'This is working','status':True,'listnum':len(lists),'img':image_base64})
    
api.add_resource(CardsAPI,'/api/allcards')

class EditCardAPI(Resource):
    @jwt_required()
    def get(self,card_id):
        current_user=get_jwt_identity()
        user = find_user(current_user)
        lists = List.query.filter_by(user_id=user.user_id).all()
        list_items=[{'id':list.id,
                        'title':list.title} for list in lists]
       
        card= Card.query.filter_by(id=card_id).first()
        deadline=card.deadline.strftime('%Y-%m-%d')
        jsonified_card={
        'title':    card.title,
        'content':    card.content,
        'list_id':card.list_id,
        }
        return {'card_data':jsonified_card,'list_items':list_items,'status':True,'deadline':deadline}
    
    
api.add_resource(EditCardAPI,'/api/editcard/<int:card_id>')