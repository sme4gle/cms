from datetime import datetime

from app import db
from models.user import User


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, unique=True, nullable=False)
    content = db.Column(db.String, nullable=False)
    short_content = db.Column(db.String, nullable=False)
    created_date = db.Column(db.DateTime, nullable=False, default=datetime.now())
    edited_date = db.Column(db.DateTime, nullable=False, default=datetime.now())
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    edited_by = db.Column(db.Integer, db.ForeignKey('user.id'))

    creator = db.relationship(
        "User",
        foreign_keys=[created_by],
    )
    editor = db.relationship(
        "User",
        foreign_keys=[edited_by],
    )