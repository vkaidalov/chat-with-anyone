from chat_with_anyone.db import db
from datetime import datetime


class GroupMessage(db.Model):
    __tablename__ = 'group_messages'

    id = db.Column(db.Integer(), primary_key=True)
    text = db.Column(db.String(length=500), nullable=False)
    created_at = db.Column(db.DateTime(), default=datetime.utcnow())
    room_id = db.Column(db.Integer, db.ForeignKey('group_rooms.id', ondelete='CASCADE'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='SET NULL'))
