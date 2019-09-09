from datetime import datetime
from chat_with_anyone.db import db


class GroupRoom(db.Model):
    __tablename__ = 'group_rooms'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=200), nullable=False)
    last_message_at = db.Column(db.DateTime(), default=datetime.utcnow)
