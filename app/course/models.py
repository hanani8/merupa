from app.database import db

class Course(db.Model):
    __tablename__ = "course"
    id = db.Column(db.String, primary_key=True, unique=True, nullable=False)
    name = db.Column(db.String, unique=True, nullable=False)
    acronym = db.Column(db.String, nullable=False)
    credits = db.Column(db.Integer, nullable=False)
    prerequisites = db.Column(db.String)
    corequisites = db.Column(db.String)
    description = db.Column(db.String)
    level = db.Column(db.String, nullable=False, default="FOUNDATIONAL")

class Rating(db.Model):
    __tablename__ = "rating"
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False, autoincrement=True)
    rtype = db.Column(db.String, unique=True, nullable=False)

from app.student.models import Student

class CourseRating(db.Model):
    __tablename__ = "course_rating"
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False, autoincrement=True)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    student_id = db.Column(db.String, db.ForeignKey('student.id'), nullable=False)
    rating_id = db.Column(db.Integer, db.ForeignKey('rating.id'), nullable=False)
    value = db.Column(db.Float, nullable=False)

class CourseFeedback(db.Model):
    __tablename__ = "course_feedback"
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False, autoincrement=True)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    student_id = db.Column(db.String, db.ForeignKey('student.id'), nullable=False)
    feedback = db.Column(db.String)
    upvote = db.Column(db.Integer, nullable=False)
    downvote = db.Column(db.Integer, nullable=False)