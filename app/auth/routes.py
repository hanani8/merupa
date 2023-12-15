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

        user = User.query.filter_by(email=username).first()
        
        if user is None:
            return {'error': True, "msg": 'Invalid Username'}, 404
        else:
            if user.password == password:
                result = login_user(user)

                user_id = user.id
                name = user.name
                email = user.email
                role = user.roles[0].name
                print(user.roles, role)
                data = {
                    "user": {
                    "id": user_id,
                    "name": name,
                    "email": email,
                    },
                    "role": role
                }

                return {"error": False, "msg": "LOGGED_IN", "data": data}, 200
            else:
                return {'message': 'Invalid credentials'}, 401
    
    def get(self):
        # Check if the user is currently logged in
        if current_user.is_authenticated:
            user_id = current_user.id
            email = current_user.email
            name = current_user.name
            role = current_user.roles[0].name
            print(current_user.roles[0].name)
            data = {
                "user": {
                "id": user_id,
                "email": email,
                "name": name
                },
                "role": role
            }
            return {"error": False, "msg": "LOGGED_IN", "data": data}, 200
        else:
            return {'error': False, 'msg': "NOT_LOGGED_IN"}, 200

    def delete(self):
        # Log out the user (destroy session)
        logout_user()
        return {'message': 'Logout successful'}, 200

# Add these resources to your Flask-RESTful API
auth_api.add_resource(LoginResource, '/api/login_user', '/api/isloggedin', '/api/logout_user')
