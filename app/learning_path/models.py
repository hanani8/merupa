from app.database import db
from app.student.models import *

class LearningPath(db.Model):
    __tablename__ = "learningpath"
    id = db.Column(db.Integer, autoincrement = True, primary_key = True)
    path = db.Column(db.String, nullable = False)
    upvote = db.Column(db.Integer, default = 0)

class LPUpvote(db.Model):
    __tablename__ = "lpupvote"
    id = db.Column(db.Integer, autoincrement = True, primary_key = True)
    user_id =  db.Column(db.Integer, db.ForeignKey("user.id"))
    learning_path_id = db.Column(db.Integer, db.ForeignKey("learningpath.id"))

