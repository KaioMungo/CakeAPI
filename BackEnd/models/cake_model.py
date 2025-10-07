from config.database import db
from errors import EmptyStringError, AuthError, IdNotExist
from datetime import datetime, timezone

class Cake(db.Model):
    __tablename__ = 'cakes'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    flavor = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text)
    date_created = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    available = db.Column(db.String(20), default="Disponivel")

    def __init__(self, name, flavor, price, description):
        self.name = name
        self.flavor = flavor
        self.price = price
        self.description = description


    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'flavor': self.flavor,
            'price': self.price,
            'description': self.description,
            'date_created': self.date_created,
            'available': self.available
        }