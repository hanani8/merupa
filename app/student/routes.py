from app.student.models import *
from flask_restful import Resource, marshal_with, reqparse, fields, marshal
from flask_security import roles_required, auth_required, current_user
from app.validation import BusinessValidationError, NotFoundError
from flask import jsonify
# from app.security import user_datastore

from . import student_api

student_fields = {
    "id": fields.Integer,
    "rollno": fields.String,
    "name": fields.String,
    "phone": fields.Integer,
    "cgpa": fields.Float,
    "completed_courses": fields.List(fields.Nested({
        "id": fields.Integer,
        "course_id": fields.String,
        "score": fields.Integer,
        "sequence": fields.Integer
    }))
}

student_response_fields = {
    "error": fields.Boolean,
    "msg": fields.String,
    "data": fields.Nested(student_fields)
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
    "sequence": fields.Integer,
}

students_courses_response_fields = {
    "error": fields.Boolean,
    "msg": fields.String,
    "data": fields.Nested(students_courses_fields)
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
    # @marshal_with(student_response_fields)
    def get(self, id=None):
        if id is None:
            students = Student.query.all()
            return marshal({"error":False,"msg":"Fetched all students successfully","data":students},student_response_fields), 200
        student = Student.query.get(id)
        if student:
            completed_courses = StudentsCourses.query.filter_by(student_id=id).all()
            student.completed_courses = completed_courses
            return marshal({"error":False,"msg":"Fetched student successfully","data":student},student_response_fields), 200
        else:
            return {"error":True,"msg":"Student Not found"}, 404
        
    # @marshal_with(student_response_fields)
    # @roles_required("admin")
    def post(self):
        args = student_parser.parse_args()
        # print("*********************************88")
        email = args.get("email",None)
        name = args.get("name",None)
        password = args.get("password",None)
        phone = args.get("phone",None)

        print(email, name, password, phone)

        if any(field is None for field in (email, name, password, phone)):
            return {"error" : True,"msg" : "One or more fields are empty"}, 400
        
        student_exist = Student.query.filter_by(email=email).first()
        if student_exist:
            return {"error" : True,"msg" : "Email already exists"}, 400
        
        student = Student(email=email,
                          name=name,
                          password=password,
                          fs_uniquifier=''.join(random.choices(string.ascii_letters,k=10)),
                          phone=phone,
                          rollno=email.split('@')[0])
        
        

        try:
            db.session.add(student)
            db.session.flush()
            db.session.commit()

            user = User.query.filter_by(id = student.id).first()
            role = Role.query.filter_by(name='student').first()

            user.roles.append(role)

            db.session.add(user)
            db.session.flush()
            db.session.commit()

            return marshal({"error":False,"msg":"Student created successfully","data":student},student_response_fields), 201
        except Exception as e:
            print(e)
            
            db.session.rollback()

            return {"error":True,"msg":"Student could not be created"}, 400

        

    
    @roles_required("admin")
    def delete(self, id):
        student = Student.query.get(id)
        if student:
            db.session.delete(student)
            db.session.commit()
            return {"error":False,"msg":"Student deleted successfully"}, 200
        else:
            return {"error":True,"msg":"Student not found"}, 404
    
    # @marshal_with(student_response_fields)
    @roles_required("admin")
    def put(self, id):
        student = Student.query.get(id)
        if student is None:
            return {"error":True,"msg":"Student not found"}, 404
        
        args = student_parser.parse_args()
        email = args.get("email",None)
        name = args.get("name",None)
        phone = args.get("phone",None)

        if any(field is None for field in (email, name, phone)):
            return {"error":True,"msg":"One or more fields are empty"}, 400
        
        student_exist = Student.query.filter_by(email=email).first()
        if student_exist and student_exist.id != student.id:
            return {"error":True,"msg":"Email already exists"}, 400

        student.email = email
        student.name = name
        student.phone = phone
        student.rollno = email.split('@')[0]

        db.session.commit()
        return marshal({"error":False,"msg":"Student edited successfully","data":student},student_response_fields), 200
    
    # @marshal_with(students_courses_response_fields)
    @roles_required("admin")
    def patch(self, id):
        student = Student.query.get(id)
        if student is None:
            return {"error":True,"msg":"Student not found"}, 404
        
        args = students_courses_parser.parse_args()
        student_id = args.get("student_id",None)
        course_id = args.get("course_id",None)
        score = args.get("score",None)
        sequence = args.get("sequence",None)

        if any(field is None for field in (course_id, score, sequence)):
            return {"error":True,"msg":"One or more fields are empty"}, 400
        
        # sc = StudentsCourses(student_id=id, course_id=course_id, score=score, sequence=sequence)
        sc = StudentsCourses.query.filter_by(student_id=id, course_id=course_id).first()
        sc.score = score

        db.session.add(sc)
        student.cgpa = cgpa(id)
        db.session.commit()
        return marshal({"error":False,"msg":"Student scores updated successfully","data":sc},students_courses_response_fields), 200
    
    # @marshal_with(students_courses_response_fields)
    def post_scores(self, id):
        student = Student.query.get(id)
        if student is None:
            return {"error":True,"msg":"Student not found"}, 404
        
        args = students_courses_parser.parse_args()
        course_id = args.get("course_id",None)
        score = args.get("score",None)
        
        result = (db.session.query(
                    StudentsCourses.student_id,
                    db.func.max(StudentsCourses.sequence).label("max_sequence")
                )
                .filter(StudentsCourses.student_id == id)
                .group_by(StudentsCourses.student_id)
                .first())
        print(result)
        sequence = result.max_sequence

        if any(field is None for field in (course_id, score)):
            return {"error":True,"msg":"One or more fields are empty"}, 400
        
        sc = StudentsCourses(student_id=id, course_id=course_id, score=score, sequence=sequence)

        db.session.add(sc)
        student.cgpa = cgpa(id)
        db.session.commit()
        return marshal({"error":False,"msg":"Student scores updated successfully","data":sc},students_courses_response_fields), 200

import_parser = reqparse.RequestParser()
import_parser.add_argument("data")

class ImportAPI(Resource):
    def post(self):
        args = import_parser.parse_args()
        data = args.get("data",None)
        for records,row in enumerate(data.split('\n')):
            row = row.split(',')
            row = ''.join(row).split()
            student_id = row[0]
            sequence = 1
            student = Student.query.get(student_id)
            for course_id in row[1::2]:
                score = row[row.index(course_id)+1]
                sc = StudentsCourses(student_id=student_id, course_id=course_id, score=score, sequence=sequence)
                sequence += 1
                db.session.add(sc)
                student.cgpa = cgpa(student_id)
        db.session.commit()
        return {"error":False, "msg":f"{records+1} records are updated successfully"}, 201
                

student_api.add_resource(StudentAPI, "/api/student/<int:id>", "/api/admin/students", "/api/admin/student", "/api/admin/student/<int:id>")
student_api.add_resource(ImportAPI, "/api/admin/import")