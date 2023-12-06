from flask_restful import Resource, reqparse
from flask_security import current_user
from app.learning_path.models import *
from app.database import db
from . import lp_api
 
create_path_parser = reqparse.RequestParser()
create_path_parser.add_argument("id", type=int)
create_path_parser.add_argument("path", type=str)
create_path_parser.add_argument("upvote", type=int)

class LearningPathsAPI(Resource):
    def get(self):
        learningpaths = LearningPath.query.all()
        l=[]
        for lps in learningpaths:
            learningpaths_json = {}
            learningpaths_json["id"] = lps.id
            lp = lps.path.split("/")
            lp.remove('')
            lp_dict = {}
            for i in range(0,len(lp)-2,2):
                courses = lp[i+1].split('_')
                courses.remove('')
                courses.remove('')
                lp_dict.update({int(lp[i]):courses})
            learningpaths_json["path"] = lp_dict
            learningpaths_json["upvote"] = lps.upvote
            l.append(learningpaths_json)
        
        return l, 200
    
class LearningPathAPI(Resource):
    def get(self, id):
        learningpath = LearningPath.query.filter_by(id = id).first()

        if learningpath is None:
            return "No Such learning path Found", 404
        else:
            learningpath_json = {}
            learningpath_json["id"] = learningpath.id
            lp = learningpath.path.split("/")
            lp.remove('')
            lp_dict = {}
            for i in range(0,len(lp)-2,2):
                courses = lp[i+1].split('_')
                courses.remove('')
                courses.remove('')
                lp_dict.update({int(lp[i]):courses})
            learningpath_json["path"] = lp_dict
            learningpath_json["upvote"] = learningpath.upvote
        
            return learningpath_json, 200
        
    def patch(self, id):
        learningpath = LearningPath.query.filter_by(id = id).first()
        upvoted = LPUpvote.query.filter_by(user_id = current_user.id, learning_path_id = learningpath.id).first()
        
        if upvoted is not None:
            learningpath.rating += 1
            new_upvote = LPUpvote(user_id = current_user.id, learning_path_id = learningpath.id)
        else:
            return "Already upvoted", 400

        try :
            db.session.add(learningpath)
            db.session.add(new_upvote)
            db.session.flush()
        except Exception as e: 
            print(e)
            db.session.rollback()
        db.session.commit()

        return "Learning path successfully upvoted", 200 


lp_api.add_resource(LearningPathsAPI, "/api/learningpaths")
lp_api.add_resource(LearningPathAPI, "/api/learningpath/<int:id>", "/api/learningpath/upvote/<int:id>")

