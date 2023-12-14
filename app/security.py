from flask_security import Security, SQLAlchemyUserDatastore, SQLAlchemySessionUserDatastore
from app.student.models import User, Role
from app.database import db

user_datastore = SQLAlchemySessionUserDatastore(db.session, User, Role)
security = Security()

@security.unauthorized_handler
def unauthorized_handler():
    return {"error": False, "msg": "NOT_LOGGED_IN"}, 200