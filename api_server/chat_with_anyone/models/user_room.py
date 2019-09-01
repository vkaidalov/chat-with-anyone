from chat_with_anyone.db import db


class UserRoom(db.Model):
    __tablename__ = 'user_rooms'

    room_id = db.Column(db.Integer, db.ForeignKey('rooms.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
