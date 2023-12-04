import os
from flask import Flask, make_response
from flask_restful import Resource, Api, marshal_with, reqparse, fields
from config import LocalDevelopmentConfig, StageConfig
from database import db
from flask_security import Security, SQLAlchemySessionUserDatastore, SQLAlchemyUserDatastore
from app.student.models import User, Role
import json
from werkzeug.exceptions import HTTPException

app = None
api = None

def create_app():
    app = Flask(__name__, template_folder="templates")
    print(os.getenv('ENV', "development"))

    if os.getenv('ENV', "development") == "production":
      app.logger.info("Currently no production config is setup.")
      raise Exception("Currently no production config is setup.")
    elif os.getenv('ENV', "development") == "stage":
      app.logger.info("Staring stage.")
      print("Staring  stage")
      app.config.from_object(StageConfig)
      print("pushed config")
    else:
      app.logger.info("Staring Local Development.")
      print("Staring Local Development")
      app.config.from_object(LocalDevelopmentConfig)
      print("pushed config")
    app.app_context().push()

    print("DB Init")
    db.init_app(app)
    print("DB Init complete")
    app.app_context().push()
    app.logger.info("App setup complete")

    db.create_all()

    # Setup Flask-Security
    user_datastore = SQLAlchemySessionUserDatastore(db.session, User, Role)
    security = Security(app, user_datastore)

    api = Api(app)
    app.app_context().push()   
    print("Create app complete")
    
    return app, api

app, api = create_app()

from app.course.models import *
course_fields = {
    "id": fields.String,
    "name": fields.String,
}

course_ratings_fields = {
  "id": fields.Integer,
  "course_id": fields.String,
  "student_id": fields.String
}

course_parser = reqparse.RequestParser()
course_parser.add_argument("id")
course_parser.add_argument("name")
course_parser.add_argument("description")
course_parser.add_argument("rating_type")
course_parser.add_argument("rating_value")
course_parser.add_argument("student_id")




class CourseApi(Resource):
    def get(self, id=None):
        if id is None:
          courses_required = Course.query.all()
          try:
            l = []
            for course_required in courses_required:
              course_json = {}
              course_json["id"] = course_required.id
              course_json["name"] = course_required.name
              course_json["description"] = course_required.description
              l.append(course_json)
            return l, 200
          except AttributeError:
            return "Invalid Course ID"
        else:
          course_required = Course.query.filter_by(id=id).first()
          try:
            course_json = {}
            course_json["id"] = course_required.id
            course_json["name"] = course_required.name
            course_json["description"] = course_required.description
            return course_json, 200
          except AttributeError:
            return "Invalid Course ID"
          
    @marshal_with(course_ratings_fields)
    def post(self, id):
      args = course_parser.parse_args()
      rating_type = args["rating_type"]
      rating_value = args["rating_value"]
      student_id = args["student_id"]
      fetched_rating = Rating.query.filter_by(type = rating_type).first()
      fetched_student = Student.query.filter_by(id = student_id).first()
      course = Course.query.filter_by(id = id).first()
      if fetched_rating is not None:
        if course is not None:
          if fetched_student is not None:
            course_rating_record = CourseRating(
                course_id = id,
                student_id = student_id,
                rating_id = fetched_rating.id,
                value = rating_value
            )
            db.session.add(course_rating_record)
            db.session.commit()
            return course_rating_record, 201 
          else:
           raise BusinessValidationError(status_code=400,error_code="S001",error_message="Student Not Found")
        else:
           raise BusinessValidationError(status_code=400,error_code="C001",error_message="Course Not Found")
      else:
         raise BusinessValidationError(status_code=400,error_code="R001",error_message="Rating Type Not Found")
      
         
      
    
       
class BusinessValidationError(HTTPException):
    def __init__(self,status_code, error_code, error_message):
        message = {"Error Code": error_code, "Message": error_message}
        self.response = make_response(json.dumps(message),status_code)  


api.add_resource(CourseApi, "/api/courses/", "/api/courses/<string:id>/", "/api/courses/<string:id>/rating")



if __name__ == '__main__':
  # Run the Flask app
  app.run(host='0.0.0.0')
