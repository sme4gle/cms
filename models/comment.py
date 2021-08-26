from datetime import datetime

from config.database import db


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    parent = db.Column(db.Integer)
    created_date = db.Column(db.DateTime, nullable=False, default=datetime.now())
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    content = db.Column(db.String)

    # Relationships
    post = db.relationship('Post', backref='comments')
    author = db.relationship('User')
