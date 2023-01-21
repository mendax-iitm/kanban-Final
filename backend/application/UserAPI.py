
from main import bcrypt
from application.api import *
from application.models import User
from application.helperfunction import userExist, emailExist
import datetime




user_fields = {
    'id':   fields.Integer,
    'username':    fields.String,
    'password':     fields.String,
    'active':    fields.Integer
}
class UserLoginAPI(Resource):
    def post(self):
        username=request.get_json()['username']
        password=request.get_json()['password']
        print(username,password)
        user = db.session.query(User).filter(User.username==username).first()
        if user is None or not bcrypt.check_password_hash(user.password,password):
            return {'status':False,'msg': 'Username or password is incorrect'}, 400
        expires = datetime.timedelta(days=5)
        access_token = create_access_token(identity=username,expires_delta=expires)
        return {'status': True,'access_token':access_token},200
api.add_resource(UserLoginAPI, "/api/login")
class UserRegisterAPI(Resource):
    def post(self):
        username=request.get_json()['username']
        email=request.get_json()['email']
        if not userExist(username) and not emailExist(email):
            user = User(username=username, email=email)
            user.password=bcrypt.generate_password_hash(request.get_json()["password"])
            db.session.add(user)
            db.session.commit()
            expires = datetime.timedelta(days=5)
            access_token=create_access_token(identity=username,expires_delta=expires )
            return {'status': True,'access_token':access_token},200
        else:
            return {'status': False,'message': 'Username or Email already exists'},401
api.add_resource(UserRegisterAPI, "/api/register")
# class UserValidateAPI(Resource):
#         def get(self):
#             pass
#         def post(self):
            
            
# class UserAPI(Resource):
#     @marshal_with(user_fields)
#     def get(self, user_id):
#         user = User.query.filter_by(id=user_id).first()
#         if user:
#             return user
#         else:
#             raise NotFoundError(status_code=404)
    
#     @marshal_with(user_fields)
#     def put(self, user_id):
#         args = update_user_parser.parse_args()
#         user = User.query.filter_by(id=user_id).first()
        
#         if not user:
#             raise NotFoundError(status_code=404)
#         username = args.get('username',None)
#         password = args.get('password',None)
#         if username is None or type(username) is not str:
#             raise BusinessValidationError(
#                 status_code=400, error_code="USER001", error_message="Username is required and should be String")
            
#         if password is None:
#             raise BusinessValidationError(
#                 status_code=400, error_code="USER002", error_message="Password is required and should be String")
#         user_exist = User.query.filter_by(username=username).first()
#         if user_exist:
#             raise AlreadyExistedError(
#                 status_code=409)
#         user.username = username
#         user.password = bcrypt.generate_password_hash(password)
#         # db.session.add(user)
#         db.session.commit()
#         return user

    # def delete(self,user_id):
    #     user = User.query.filter_by(id=user_id).first()
    #     if user:
    #         decks = Deck.query.filter_by(user_id=user_id).all()
            
    #         for deck in decks:
    #             cards = Card.query.filter_by(deck_id=deck.id).all()
    #             for card in cards:
    #                 db.session.delete(card)
    #             db.session.delete(deck)
    #         db.session.delete(user)
    #         db.session.commit()
    #     else:
    #         raise NotFoundError(status_code=404)
    



