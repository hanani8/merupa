from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, SQLAlchemyUserDatastore
from flask_restful import Resource, Api
from app.student.models import User, Role
from config import LocalDevelopmentConfig, StageConfig

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
    # Setup Flask-Security
    user_datastore = SQLAlchemySessionUserDatastore(db.session, User, Role)
    security = Security(app, user_datastore)
    api = Api(app)
    app.app_context().push()   
    
    # # Create celery   
    # celery = workers.celery

    # # Update with configuration
    # celery.conf.update(
    #     broker_url = app.config["CELERY_BROKER_URL"],
    #     result_backend = app.config["CELERY_RESULT_BACKEND"]
    # )

    # celery.Task = workers.ContextTask
    # app.app_context().push()
    # cache = Cache(app)
    # app.app_context().push()
    print("Create app complete")
    return app, api

app, api = create_app()


if __name__ == '__main__':
  # Run the Flask app
  app.run(host='0.0.0.0',port=8080)
