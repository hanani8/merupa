import os
from flask import Flask, make_response
from flask_restful import Api
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
    global api
    api = Api(app)
    app.app_context().push()   
    print("Create app complete")
    
    return app, api


app, api = create_app()
     
class BusinessValidationError(HTTPException):
    def __init__(self,status_code, error_code, error_message):
        message = {"Error Code": error_code, "Message": error_message}
        self.response = make_response(json.dumps(message),status_code)  

# from app.course.routes import CourseApi
# api.add_resource(CourseApi, "/api/courses/", "/api/courses/<string:id>/", "/api/courses/<string:id>/rating")

# from app.course.routes import api

if __name__ == '__main__':
  # Run the Flask app
  app.run(host='0.0.0.0')
