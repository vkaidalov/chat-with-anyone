from datetime import datetime
from chat_with_anyone.db import db


class GroupRoom(db.Model):
    __tablename__ = 'group_rooms'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=200), nullable=False)
    last_message_at = db.Column(db.DateTime(), default=datetime.utcnow)
    last_message_text = db.Column(db.String(length=500), nullable=True)

    def __init__(self, **kw):
        super().__init__(**kw)
        self._members = set()

    @property
    def members(self):
        return self._members

    @members.setter
    def add_member(self, member):
        self._members.add(member)
        member._rooms.add(self)
