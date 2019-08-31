from datetime import datetime

from chat_with_anyone.db import db
from sqlalchemy import or_

from .contact import Contact


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

    def __init__(self, **kw):
        super().__init__(**kw)
        self._contacts = set()

    @property
    def contacts(self):
        return self._contacts

    @contacts.setter
    def add_contact(self, user):
        self._contacts.add(user)
        user._contacts.add(self)

    async def delete_relations(self):
        await Contact.delete.where(
            or_(
                Contact.owner_id == self.id,
                Contact.contact_id == self.id
            )
        ).gino.status()
