from chat_with_anyone.db import db


class GroupMempership(db.Model):
    __tablename__ = 'group_memberships'
    __table_args__ = (
        db.UniqueConstraint(
            'user_id', 'room_id', name='unique_user_room')
    )

    room_id = db.Column(db.Integer, db.ForeignKey('group_rooms.id', ondelete='CASCADE'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'))
