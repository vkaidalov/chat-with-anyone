from chat_with_anyone.db import db
from datetime import datetime


class Message(db.Model):
    __tablename__ = 'messages'

    id = db.Column(db.Integer(), primary_key=True)
    text = db.Column(db.String(length=500), nullable=False)
    created_at = db.Column(db.DateTime(), server_default=datetime.utcnow())
    room_id = db.Column(db.Integer, db.ForeignKey('rooms.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
