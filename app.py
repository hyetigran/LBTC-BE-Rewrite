from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from marshmallow import ValidationError
from dotenv import load_dotenv

from db import db
from ma import ma
from blacklist import BLACKLIST
from resources.user import (
    UserRegister,
    UserLogin,
    TokenRefresh,
    UserLogout,
)
from resources.confirmation import Confirmation, ConfirmationByUser
from resources.offer import OfferList, Offer, OfferCreate, UserOfferList

app = Flask(__name__)
load_dotenv(".env", verbose=True)
app.config.from_object("default_config")  # load default configs from default_config.py
app.config.from_envvar(
    "APPLICATION_SETTINGS"
)  # override with config.py (APPLICATION_SETTINGS points to config.py)
api = Api(app)
jwt = JWTManager(app)
db.init_app(app)  # remove after migrations
ma.init_app(app)  # remove after migrations
migrate = Migrate(app, db)


@app.before_first_request
def create_tables():
    db.create_all()


@app.errorhandler(ValidationError)
def handle_marshmallow_validation(err):
    return jsonify(err.messages), 400


@jwt.token_in_blocklist_loader
def check_if_token_in_blacklist(decrypted_token):
    return decrypted_token["jti"] in BLACKLIST


api.add_resource(UserRegister, "/register")
api.add_resource(UserLogin, "/login")
api.add_resource(TokenRefresh, "/refresh")
api.add_resource(UserLogout, "/logout")
api.add_resource(Confirmation, "/user_confirm/<string:confirmation_id>")
api.add_resource(ConfirmationByUser, "/confirmation/user/<int:user_id>")
api.add_resource(OfferCreate, "/offer")
api.add_resource(Offer, "/offer/<int:user_id>/<int:offer_id>")
api.add_resource(OfferList, "/offers")
api.add_resource(UserOfferList, "/offers/<int:user_id>")

if __name__ == "__main__":
    db.init_app(app)
    ma.init_app(app)
    app.run(port=5000, debug=True)
