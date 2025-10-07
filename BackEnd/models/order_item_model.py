from datetime import datetime, timezone
from config.database import db


class OrderItem(db.Model):
    __tablename__ = 'order_items'

    order_item_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    cake_id = db.Column(db.Integer, db.ForeignKey('cakes.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    unit_price = db.Column(db.Float, nullable=False)

    order = db.relationship('Order', backref=db.backref('items', lazy=True))
    cake = db.relationship('Cake', backref=db.backref('order_usages', lazy=True))

    def __init__(self, order_id, cake_id, quantity, unit_price):
        self.order_id = order_id
        self.cake_id = cake_id
        self.quantity = quantity
        self.unit_price = unit_price

    def to_dict(self):
        return {
            'order_item_id': self.order_item_id,
            'order_id': self.order_id,
            'cake_id': self.cake_id,
            'quantity': self.quantity,
            'unit_price': self.unit_price
        }