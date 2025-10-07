from datetime import datetime, timezone
from config.database import db


class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    order_date = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), default="Pendente", nullable=False)
    delivery_date = db.Column(db.DateTime, nullable=True)

    customer = db.relationship('Customer', backref=db.backref('orders', lazy=True))

    def __init__(self, customer_id, total_price, delivery_date=None, status="Pendente"):
        self.customer_id = customer_id
        self.total_price = total_price
        self.delivery_date = delivery_date
        self.status = status

    def to_dict(self):
        return {
            'id': self.id,
            'customer_id': self.customer_id,
            'order_date': self.order_date,
            'total_price': self.total_price,
            'status': self.status,
            'delivery_date': self.delivery_date
        }