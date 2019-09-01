from chat_with_anyone.db import db
from datetime import datetime


class Room(db.Model):
    __tablename__ = 'rooms'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=200))
    description = db.Column(db.String(length=1000))
    last_message_at = db.Column(db.DateTime(), server_default=datetime.utcnow())
