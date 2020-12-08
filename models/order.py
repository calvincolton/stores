import os
from db import db
from typing import List
import stripe


CURRENCY = "usd"


class ItemsInOrder(db.Model):
    __tablename__ = "items_in_order"

    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey("items.id"))
    order_id = db.Column(db.Integer, db.ForeignKey("orders.id"))
    quantity = db.Column(db.Integer)

    item = db.relationship("ItemModel")
    order = db.relationship("OrderModel", back_populates="items")


class OrderModel(db.Model):
    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(20), nullable=False)

    items = db.relationship("ItemsInOrder", back_populates="order")

    @classmethod
    def find_all(cls) -> List["OrderModel"]:
        return cls.query.all()

    @classmethod
    def find_by_id(cls, _id: int) -> "OrderModel":
        return cls.query.filter_by(id=_id).first()

    @property
    def description(self):
        """
        Generates a simple string representing the oder, in the format of "5x chars, 2x tables"
        """
        item_counts = [f"{i.quantity}x {i.item.name}" for i in self.items]
        return ",".join(item_counts)

    @property
    def amount(self):
        return int(
            sum([item_data.item.price * item_data.quantity for item_data in self.items])
            * 100
        )

    def charge_with_stripe(self, token: str) -> stripe.Charge:
        stripe.api_key = os.getenv("STRIPE_PUBLISHABLE_KEY")

        return stripe.Charge.create(
            amount=self.amount,  # amount in USD cents (e.g. 100 = $1)
            currency=CURRENCY,
            description=self.description,
            source=token,
        )

    def set_status(self, new_status: str) -> None:
        self.status = new_status
        self.save_to_db()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()