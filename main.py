import os
from flask import Flask, make_response
from flask_restful import Api
from app.config import LocalDevelopmentConfig, StageConfig
from app.database import db
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
    global api
    api = Api(app)
    app.app_context().push()   
    print("Create app complete")
    
    return app, api

app, api = create_app()
     
from app.course.routes import CourseApi, CourseRatingApi
from app.student.routes import StudentAPI
api.add_resource(CourseApi, "/api/courses/", "/api/courses/<string:id>/")
api.add_resource(CourseRatingApi, "/api/courses/<string:id>/rating")
api.add_resource(StudentAPI, "/api/student/<int:student_id>", "/api/admin/students")
from app.learning_path.routes import LearningPathAPI, LearningPathsAPI
api.add_resource(LearningPathsAPI, "/api/learningpaths")
api.add_resource(LearningPathAPI, "/api/learningpath/<int:id>", "/api/learningpath/upvote")

if __name__ == '__main__':
  # Run the Flask app
  app.run(host='0.0.0.0')
