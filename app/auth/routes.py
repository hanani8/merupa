from flask_restful import Resource, reqparse
from flask_security import auth_required, current_user, logout_user, login_user
from . import auth_api
from app.student.models import User, Role

auth_parser = reqparse.RequestParser()
auth_parser.add_argument("username")
auth_parser.add_argument("password")

class LoginResource(Resource):
    def post(self):
        args = auth_parser.parse_args()
        username = args.get('username')
        password = args.get('password')

        print(username, password)

        user = User.query.filter_by(email=username).first()
        
        if user is None:
            return {'error': True, msg: 'Invalid Username'}, 404
        else:
            if user.password == password:
                result = login_user(user)
                return {'message': 'Login successful'}, 200
            else:
                return {'message': 'Invalid credentials'}, 401
    
    def get(self):
        # Check if the user is currently logged in
        if current_user.is_authenticated:
            return {"error": False, "msg": "LOGGED_IN"}, 200
        else:
            return {'error': False, 'msg': "NOT_LOGGED_IN"}, 200

    def delete(self):
        # Log out the user (destroy session)
        logout_user()
        return {'message': 'Logout successful'}, 200

# Add these resources to your Flask-RESTful API
auth_api.add_resource(LoginResource, '/api/login_user', '/api/isloggedin', '/api/logout_user')
