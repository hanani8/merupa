
class LearningPath(db.Model):
    __tablename__ = "learningpath"
    id = db.Column(db.Integer, autoincrement = True, primary_key = True)
    path = db.Column(db.String, nullable = False)
    rating = db.Column(db.Integer)
