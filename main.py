import os
from flask import Flask
from flask_restful import Resource, Api, marshal_with, reqparse, fields
from config import LocalDevelopmentConfig, StageConfig
from database import db
from flask_security import Security, SQLAlchemySessionUserDatastore, SQLAlchemyUserDatastore
from app.student.models import User, Role
import json

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
    "acronym": fields.String,
    "credits": fields.Integer,
    "prerequisites": fields.String,
    "corequisites": fields.String,
    "description": fields.String
}

course_parser = reqparse.RequestParser()
course_parser.add_argument("id")
course_parser.add_argument("name")
course_parser.add_argument("description")

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
          
    @marshal_with(course_fields)
    def post(self):
            
    
       
       

api.add_resource(CourseApi, "/api/courses/", "/api/courses/<string:id>/")



if __name__ == '__main__':
  # Run the Flask app
  app.run(host='0.0.0.0')
