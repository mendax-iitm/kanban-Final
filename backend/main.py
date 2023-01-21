
# from flask_login import LoginManager
from flask_cors import CORS
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from application import workers
from flask_caching import Cache
import os
from flask import Flask
from flask_restful import Resource, Api
from application import config
from application.config import LocalDevelopmentConfig
from application.database import db
from flask_bcrypt import Bcrypt
# from flask_security import (
#     Security,
#     SQLAlchemySessionUserDatastore,
#     SQLAlchemyUserDatastore,
# )




# app = Flask(__name__, template_folder="templates")
app = Flask(__name__)
if os.getenv("ENV", "development") == "production":
    raise Exception("Currently no production config is setup.")
else:
    print("Staring Local Development")
    app.config.from_object(LocalDevelopmentConfig)
db.init_app(app)
app.app_context().push()

CORS(app)
app.app_context().push()
celery=workers.celery
celery.conf.update(
broker_url = app.config["CELERY_BROKER_URL"],
result_backend = app.config["CELERY_RESULT_BACKEND"]
    )   
celery.Task = workers.ContextTask
app.app_context().push()
cache=Cache(app)
app.app_context().push()
api = Api(app)
app.app_context().push()
bcrypt=  Bcrypt(app)
app.app_context().push()
# security=Security(app)
jwt=JWTManager(app)
app.app_context().push()
# login_manager = LoginManager(app)


# login_manager.login_view='login'


from application.models import User, Card, List

# Import all the controllers so they are loaded
from application.UserAPI import *
from application.CardAPI import *
from application.ListAPI import *
from application.controllers import *

# Add all restful controllers


# @app.errorhandler(404)
# def page_not_found(e):
#     return render_template("404.html"), 404


# @app.errorhandler(403)
# def page_not_found(e):
#     return render_template("403.html"), 403




# from application.UserAPI import *
# # from application.DeckAPI import DeckAPI
# # from application.CardAPI import CardAPI, CardsAPI
# # api.add_resource(UserAPI, "/api/user", "/api/user/<int:user_id>")
# # api.add_resource(DeckAPI, "/api/deck/<int:deck_id>", "/api/deck/user/<int:user_id>")
# # api.add_resource(CardAPI, "/api/card/<int:card_id>", "/api/card/deck/<int:deck_id>")
# # api.add_resource(CardsAPI,"/api/cards/user/<int:user_id>")
# api.add_resource(UserLoginAPI, "/api/login")
# # api.add_resource(UserValidateAPI, "/api/val")
# api.add_resource(UserRegisterAPI, "/api/register")
if __name__ == "__main__":
    # Run the Flask app
    app.run(debug=True,host='127.0.0.1',port=8081)
