from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager
from marshmallow import ValidationError
from dotenv import load_dotenv

from ma import ma
from db import db
from blacklist import BLACKLIST
from resources.user import UserRegister, UserLogin, User, TokenRefresh, UserLogout, UserConfirm

app = Flask(__name__)
load_dotenv(".env", verbose=True)
api = Api(app)


@app.before_first_request
def create_tables():
    db.create_all()

@app.errorhandler(ValidationError)
def handle_marshmallow_validation(err):
    return jsonify(err.messages), 400


jwt = JWTManager(app)

@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    return (
        decrypted_token["jti"] in BLACKLIST
    )

api.add_resource(UserRegister, "/register")
api.add_resource(User, "/user/<int:user_id>")
api.add_resource(UserLogin, "/login")
api.add_resource(TokenRefresh, "/refresh")
api.add_resource(UserLogout, "/logout")
api.add_resource(UserConfirm, "/user_confirm/<int:user_id>")

if __name__ == "__main__":
    db.init_app(app)
    ma.init_app(app)
    app.run(port=5000, debug=True)
