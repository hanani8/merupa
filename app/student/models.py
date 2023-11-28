from flask_security import UserMixin, RoleMixin
from database import db

class Role(db.Model, RoleMixin):
    __tablename__ = 'role'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String, nullable=False, unique=True)
    name = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    active = db.Column(db.Boolean)
    fs_uniquifier = db.Column(db.String, nullable=False, unique=True)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)
    
class Admin(db.Model):
    __tablename__ = 'admin'
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True, autoincrement=True)

class Student(db.Model):
    __tablename__ = 'student'
    id = db.Column(db.Integer, db.ForeignKey('user.id'),primary_key=True, autoincrement=True)
    phone = db.Column(db.Integer, nullable=False)
    rollno = db.Column(db.String, nullable=False, unique=True)
    cgpa = db.Column(db.Float, nullable=False)
    completed_courses = db.relationship('Score', backref='student',cascade='all,delete-orphan')