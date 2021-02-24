from ma import ma
from models.offer import OfferModel


class OfferSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = OfferModel
        dump_only = ("id",)
        load_instance = True
        include_fk = True
