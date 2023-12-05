from app.student.models import *
from flask import make_response
from flask_restful import Resource, marshal_with, reqparse, fields
from app.validation import BusinessValidationError

student_fields = {
    "id": fields.Integer,
    "rollno": fields.String,
    "name": fields.String,
    "phone": fields.Integer,
    "cgpa": fields.Float,
}

class StudentAPI(Resource):
    @marshal_with(student_fields)
    def get(self, student_id = None):
        if student_id is None:
            students = Student.query.all()
            return students, 201
        student = Student.query.get(student_id)
        return student,201