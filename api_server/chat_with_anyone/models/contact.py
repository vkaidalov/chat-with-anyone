from chat_with_anyone.db import db


class Contact(db.Model):
    __tablename__ = 'contacts'
    __table_args__ = (
        db.UniqueConstraint(
            'owner_id', 'contact_id', name='contacts_owner_contact')
    )

    owner_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'))
    contact_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'))
