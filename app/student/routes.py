from app.student.models import *
from flask import make_response
from flask_restful import Resource, marshal_with, reqparse, fields
from app.validation import BusinessValidationError, NotFoundError

from . import student_api

student_fields = {
    "id": fields.Integer,
    "rollno": fields.String,
    "name": fields.String,
    "phone": fields.Integer,
    "cgpa": fields.Float,
}

# student_response_fields = {
#     "error": fields.Boolean,
#     "msg": fields.String,
#     "data": fields.Nested(student_fields)
# }
student_parser = reqparse.RequestParser()
student_parser.add_argument("email")
student_parser.add_argument("name")
student_parser.add_argument("password")
student_parser.add_argument("phone")
student_parser.add_argument("rollno")
student_parser.add_argument("cgpa")

class StudentAPI(Resource):
    @marshal_with(student_fields)
    def get(self, id=None):
        if id is None:
            students = Student.query.all()
            return students, 200
        student = Student.query.get(id)
        if student:
            return student, 200
        else:
            raise NotFoundError(status_code=404)
        
    @marshal_with(student_fields)
    def post(self):
        args = student_parser.parse_args()
        email = args.get("email",None)
        name = args.get("name",None)
        password = args.get("password",None)
        phone = args.get("phone",None)
        cgpa = args.get("cgpa",None)

        if any(field is None for field in (email, name, password, phone, cgpa)):
            raise BusinessValidationError(status_code=400,error_code="S002",error_message="one or more fields are empty")
        
        student_exist = Student.query.filter_by(email=email).first()
        if student_exist:
            raise BusinessValidationError(status_code=400,error_code="S003",error_message="email already exists")
        
        student = Student(email=email,
                          name=name,
                          password=password,
                          phone=phone,
                          rollno=email.split('@')[0],
                          cgpa=cgpa)
        
        db.session.add(student)
        db.session.commit()
        return student, 201
    
    def delete(self, id):
        student = Student.query.get(id)
        if student:
            db.session.delete(student)
            db.session.commit()
            return "Student deleted successfully", 200
        else:
            raise NotFoundError(status_code=404)

        
student_api.add_resource(StudentAPI, "/api/student/<int:id>", "/api/admin/students", "/api/admin/student/<int:id>", "/api/admin/student")