from main import bcrypt
from application.api import *
from application.models import User, List, Card

from application.helperfunction import *

list_fields = {
    'id':   fields.Integer,
    'title':    fields.String,
    'user_id':fields.Integer,
    
}
create_list_parser = reqparse.RequestParser()
create_list_parser.add_argument('title', type=str, required=True)

update_list_parser = reqparse.RequestParser()
update_list_parser.add_argument('title', type=str, required=True)

class ListAPI(Resource):
    @jwt_required()
    def get(self):
        current_user=get_jwt_identity()
        user = find_user(current_user)
        if not user:
            return{'status':False,'error_message':'User not found'},401
            
        lists = find_all_list(user.user_id)
        if len(lists)==0:
            return{'status':False,'error_message':'List not created for the user'},200
        else:
            return  {"lists":[{
            "id": list.id,
            "title": list.title,
            "user_id": list.user_id,
        } for list in lists]}
    @jwt_required()
    def put(self, list_id):
        list= List.query.filter_by(id=list_id).first()
        if not list:
            return{'status':False,'error_message':'List not found'},401
        user_id = list.user_id
        user = User.query.filter_by(user_id=user_id).first()
        args = update_list_parser.parse_args()
        title = args.get('title',None)
        if title is None or type(title) is not str or len(title)==0:
            return{'status':False,'error_message':"Title should be non-empty string"}      
        list_exist =List.query.filter((List.title==title) & (List.user_id==user_id)).first()
        if list_exist:
            return{'status':False,'error_message':"The title already exists"}
        
        list.title=title
        db.session.commit()
        
        return {'title':list.title,'status':True}
    @jwt_required()   
    def delete(self,list_id):
        list= List.query.filter_by(id=list_id).first()
        if not list:
            return{'status':False,'error_message':'List not found'},401
        cards = Card.query.filter_by(list_id=list_id).all()
        for card in cards:
            db.session.delete(card)
        db.session.delete(list)
        db.session.commit()
        return {'status':True}
    @jwt_required()
    def post(self):
        current_user=get_jwt_identity()
        print(current_user)
        user = User.query.filter_by(username=current_user).first()
        if not user:
            return{'status':False,'error_message':'User not found'},401
        args = create_list_parser.parse_args()
        title = args.get('title',None)
        if title is None or type(title) is not str or len(title)==0:
            return{'status':False,'error_message':"Title should be non-empty string"}
        list_exist =List.query.filter((List.title==title) & (List.user_id==user.user_id)).first()
        if list_exist:
            return{'status':False,'error_message':"The title already exists"}
        
        list=List(title=title, user_id=user.user_id)
        db.session.add(list)
        db.session.commit()
        
        return {'status':True,'error_message':'The title already exists'}
api.add_resource(ListAPI,"/api/lists","/api/list/<int:list_id>",'/api/list')