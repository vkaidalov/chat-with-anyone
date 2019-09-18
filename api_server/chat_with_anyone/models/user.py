from datetime import datetime

from chat_with_anyone.db import db


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer(), primary_key=True)
    first_name = db.Column(db.String(length=30))
    last_name = db.Column(db.String(length=150))
    username = db.Column(db.String(length=40), unique=True, nullable=False)
    email = db.Column(db.String(length=255), unique=True, nullable=False)
    password = db.Column(db.String(length=255), nullable=False)
    created_at = db.Column(db.DateTime(), default=datetime.utcnow)
    is_active = db.Column(db.Boolean(), nullable=False, server_default='FALSE')
    token = db.Column(db.String(length=40), nullable=False, unique=True)
    token_created_at = db.Column(db.DateTime(), default=datetime.utcnow)

    def __init__(self, **kw):
        super().__init__(**kw)
        self._contacts = set()
        self._rooms = set()

    @property
    def contacts(self):
        return self._contacts

    @property
    def rooms(self):
        return self._rooms

    @contacts.setter
    def add_contact(self, user):
        self._contacts.add(user)
        user._contacts.add(self)

    @rooms.setter
    def add_room(self, room):
        self._rooms.add(room)
        room._members.add(self)
