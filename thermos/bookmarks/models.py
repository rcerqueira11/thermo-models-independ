from datetime import datetime
from sqlalchemy import desc
from thermos import db
from werkzeug.security import check_password_hash, generate_password_hash

from flask_login import UserMixin
from thermos.auth.models import User

tags = db.Table('bookmark_tag',
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')),
    db.Column('bookmark_id', db.Integer, db.ForeignKey('bookmark.id'))
)


class Bookmark(db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default = datetime.utcnow)
    description = db.Column(db.String(300))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    _tags = db.relationship('Tag',secondary=tags, lazy='joined',
                            backref = db.backref('bookmarks', lazy='dynamic'))

    @staticmethod
    def newest(num):
        return Bookmark.query.order_by(desc(Bookmark.date)).limit(num)

    @property
    def tags(self):
        return ",".join([t.name for t in self._tags])

    @tags.setter
    def tags(self,string):
        if string:
            self._tags = [Tag.get_or_create(name) for name in string.split(',')]
        else:
            self._tags = []
    def __repr__(self):
        return "<Bookmark '{}': '{}'>".format(self.description,self.url)


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25), nullable=False, unique=True, index=True)

    @staticmethod
    def get_or_create(name):
        try:
            return Tag.query.filter_by(name=name).one()
        except:
            return Tag(name=name)

    @staticmethod
    def all():
        return Tag.query.all()

    def __repr__(self):
        return self.name