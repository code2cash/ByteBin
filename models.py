from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

content_tags = db.Table(
    'content_tags',
    db.Column('content_id',
              db.Integer,
              db.ForeignKey('content.id'),
              primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True))


class Content(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content_type = db.Column(db.String(10), nullable=False)
    content = db.Column(db.Text, nullable=True)
    file_path = db.Column(db.String(255), nullable=True)
    short_url = db.Column(db.String(10), unique=True, nullable=False)
    file_type = db.Column(db.String(10), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    views = db.Column(db.Integer, default=0)
    shares = db.Column(db.Integer, default=0)
    tags = db.relationship('Tag',
                           secondary=content_tags,
                           backref=db.backref('contents', lazy='dynamic'))

    def __repr__(self):
        return f'<Content {self.id}>'


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Tag {self.name}>'


class Analytics(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content_id = db.Column(db.Integer,
                           db.ForeignKey('content.id'),
                           nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    action_type = db.Column(db.String(10), nullable=False)

    content = db.relationship('Content',
                              backref=db.backref('analytics', lazy=True))

    def __repr__(self):
        return f'<Analytics {self.id}>'
