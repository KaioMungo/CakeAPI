from datetime import datetime, timezone
from config.database import db
from datetime import datetime, timezone


class Customer(db.Model):
    __tablename__ = 'customers'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=True) # Adicionei unique para o email
    phone = db.Column(db.String(20), nullable=True)
    address = db.Column(db.Text)
    date_created = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def __init__(self, name, email=None, phone=None, address=None):
        self.name = name
        self.email = email
        self.phone = phone
        self.address = address

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'address': self.address,
            'date_created': self.date_created
        }