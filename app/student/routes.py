from app.student.models import *
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

student_parser = reqparse.RequestParser()
student_parser.add_argument("email")
student_parser.add_argument("name")
student_parser.add_argument("password")
student_parser.add_argument("phone")
student_parser.add_argument("rollno")

students_courses_fields = {
    "id": fields.Integer,
    "student_id": fields.Integer,
    "course_id": fields.String,
    "score": fields.Integer,
    "sequence": fields.Integer
}

students_courses_parser = reqparse.RequestParser()
students_courses_parser.add_argument("course_id")
students_courses_parser.add_argument("score")
students_courses_parser.add_argument("sequence")

def cgpa(student_id):
    scs = StudentsCourses.query.filter_by(student_id=student_id).all()
    credits = 0
    grades = 0
    for row in scs:
        grade = 0
        credit = 0
        score = int(row.score)
        if score >= 90:
            grade = 10
        elif score >= 80:
            grade = 9
        elif score >= 70:
            grade = 8
        elif score >= 60:
            grade = 7
        elif score >= 50:
            grade = 6
        else:
            grade = 4
        credit = int(Course.query.filter_by(id=row.course_id).first().credits)

        grades += (grade*credit)
        credits += credit
    return round((grades/credits),2)

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

        if any(field is None for field in (email, name, password, phone)):
            raise BusinessValidationError(status_code=400,error_code="S001",error_message="one or more fields are empty")
        
        student_exist = Student.query.filter_by(email=email).first()
        if student_exist:
            raise BusinessValidationError(status_code=400,error_code="S002",error_message="email already exists")
        
        student = Student(email=email,
                          name=name,
                          password=password,
                          fs_uniquifier=''.join(random.choices(string.ascii_letters,k=10)),
                          phone=phone,
                          rollno=email.split('@')[0])
        
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
    
    @marshal_with(student_fields)
    def put(self, id):
        student = Student.query.get(id)
        if student is None:
            raise NotFoundError(status_code=404)
        
        args = student_parser.parse_args()
        email = args.get("email",None)
        name = args.get("name",None)
        phone = args.get("phone",None)

        if any(field is None for field in (email, name, phone)):
            raise BusinessValidationError(status_code=400,error_code="S001",error_message="one or more fields are empty")

        student.email = email
        student.name = name
        student.phone = phone
        student.rollno = email.split('@')[0]

        db.session.commit()
        return student
    
    @marshal_with(students_courses_fields)
    def patch(self, id):
        student = Student.query.get(id)
        if student is None:
            raise NotFoundError(status_code=404)
        
        args = students_courses_parser.parse_args()
        course_id = args.get("course_id",None)
        score = args.get("score",None)
        sequence = args.get("sequence",None)

        if any(field is None for field in (course_id, score, sequence)):
            raise BusinessValidationError(status_code=400,error_code="S001",error_message="one or more fields are empty")
        
        sc = StudentsCourses(student_id=id, course_id=course_id, score=score, sequence=sequence)

        db.session.add(sc)
        student.cgpa = cgpa(id)
        db.session.commit()
        return sc

        
student_api.add_resource(StudentAPI, "/api/student/<int:id>", "/api/admin/students", "/api/admin/student", "/api/admin/student/<int:id>")