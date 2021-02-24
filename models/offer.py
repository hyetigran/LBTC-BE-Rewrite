from db import db
from typing import List


class OfferModel(db.Model):
    __tablename__ = "offers"

    id = db.Column(db.Integer, primary_key=True)
    buy_bch = db.Column(db.Boolean, nullable=False)
    country = db.Column(db.String(40), nullable=False)
    city = db.Column(db.String(80), nullable=False)
    payment_method = db.Column(db.String(40), nullable=False)
    currency_type = db.Column(db.String(40), nullable=False)
    dynamic_pricing = db.Column(db.Boolean, nullable=False)
    margin = db.Column(db.Float, nullable=False)
    margin_above = db.Column(db.Boolean, nullable=False)
    market_exchange = db.Column(db.String(40), nullable=False)
    limit_min = db.Column(db.Integer)
    limit_max = db.Column(db.Integer)
    headline = db.Column(db.String(200), nullable=False)
    trade_terms = db.Column(db.String(1000))
    open_hours = db.Column(db.DateTime)
    close_hours = db.Column(db.DateTime)
    verified_only = db.Column(db.Boolean, nullable=False)
    pause = db.Column(db.Boolean, default=False)
    maker_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    user = db.relationship("UserModel")

    @classmethod
    def find_by_id(cls, _id: int) -> "OfferModel":
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_all(cls) -> List["OfferModel"]:
        return cls.query.all()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self, _id: int) -> None:
        db.session.delete(self)
        db.session.commit()
