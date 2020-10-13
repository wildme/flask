from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask import current_app
from . import db, login_manager
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from datetime import datetime

now = datetime.now()
dt_str = now.strftime('%Y-%m-%d %H:%M:%S')

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.SmallInteger, primary_key=True, autoincrement=True)
    login = db.Column(db.String(20), unique=True)
    password_h = db.Column(db.String(128))
    firstname = db.Column(db.String(30))
    lastname = db.Column(db.String(30))
    email = db.Column(db.String(64))
    administrator = db.Column(db.Boolean)
    dep_id = db.Column(db.SmallInteger, db.ForeignKey('departments.id'))
    outbox = db.relationship('Outbox', backref='out')

    def __repr__(self):
        return '<User %r>' % self.login

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_h = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_h, password)

class Departments(db.Model):
    __tablename__ = 'departments'
    id = db.Column(db.SmallInteger, primary_key=True, autoincrement=True)
    name = db.Column(db.String(30))
    users = db.relationship('User', backref='dep')
    
    def __repr__(self):
        return '<Name %r>' % self.name

class Outbox(db.Model):
    __tablename__ = 'outbox'
    id = db.Column(db.SmallInteger, primary_key=True, autoincrement=True)
    subject = db.Column(db.String(256))
    recipient = db.Column(db.String(128))
    reg_date = db.Column(db.DateTime(), default=dt_str)
    user_id = db.Column(db.SmallInteger, db.ForeignKey('users.id'))
    attachment = db.Column(db.String(128))
    notes = db.Column(db.String(256))

    def __repr__(self):
        return '<Name %r>' % self.subject

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
