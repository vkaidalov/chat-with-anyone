from chat_with_anyone.db import db


class Contact(db.Model):
    __tablename__ = 'contacts'

    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    contact_id = db.Column(db.Integer, db.ForeignKey('users.id'))
