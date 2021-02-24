import traceback
from flask_restful import Resource
from flask import request
from flask_jwt_extended import jwt_required
from typing import List

from models.offer import OfferModel
from models.user import UserModel
from schemas.offer import OfferSchema
from libs.strings import gettext

offer_schema = OfferSchema()
offer_list_schema = OfferSchema(many=True)


class Offer(Resource):
    @classmethod
    def get(cls, user_id: int, offer_id: int):
        offer = OfferModel.find_by_id(offer_id)
        if not offer:
            return {"message": gettext("offer_not_found")}, 404

        return offer_schema.dump(offer), 200

    @classmethod
    @jwt_required(refresh=True)
    def put(cls, user_id: int, offer_id: int):
        offer_json = request.get_json()
        offer = OfferModel.find_by_id(offer_id)
        if not offer:
            return {"message": gettext("offer_not_found")}, 400
        offer = offer_schema.load(offer_json)

        try:
            offer.save_to_db()
        except:
            return {"message", gettext("offer_error_updating")}, 500

        return offer_schema.dump(offer), 200

    @classmethod
    @jwt_required(refresh=True)
    def delete(cls, user_id: int, offer_id: int):
        offer = OfferModel.find_by_id(offer_id)
        if offer:
            offer.delete_from_db()
            return {"message": gettext("offer_deleted")}, 200
        return {"message": gettext("offer_not_found")}, 400


class OfferCreate(Resource):
    @classmethod
    @jwt_required(refresh=True)
    def post(cls):
        offer_json = request.get_json()
        offer = offer_schema.load(offer_json)

        try:
            offer.save_to_db()
            return {"message": gettext("offer_created")}, 201
        except:
            traceback.print_exc()
            offer.delete_from_db()
            return {"message": gettext("offer_error_creating")}, 500


class OfferList(Resource):
    @classmethod
    def get(cls):
        return {"all_offers": offer_list_schema.dump(OfferModel.find_all())}, 200


class UserOfferList(Resource):
    @classmethod
    @jwt_required()
    def get(cls, user_id: int) -> List["OfferModel"]:
        user = UserModel.find_by_id(user_id)
        if not user:
            return {"message": gettext("user_not_found")}, 400
        return {
            "my_offers": offer_list_schema.dump(OfferModel.find_by_user(user_id))
        }, 200
