from flask_security import UserMixin, RoleMixin
from app.database import db

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
    
class Admin(User, db.Model):
    __tablename__ = 'admin'
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)

class Student(User, db.Model):
    __tablename__ = 'student'
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    phone = db.Column(db.Integer, nullable=False)
    rollno = db.Column(db.String, nullable=False, unique=True)
    cgpa = db.Column(db.Float, nullable=False)
    completed_courses = db.relationship('StudentsCourses', backref='student',cascade='all,delete-orphan')

from app.course.models import Course

class StudentsCourses(db.Model):
    __tablename__ = 'students_courses'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'))
    course_id = db.Column(db.String, db.ForeignKey('course.id'))
    score = db.Column(db.Integer, nullable=False)
    sequence = db.Column(db.Integer, nullable=False)

