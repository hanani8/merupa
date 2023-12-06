from app.course.models import *
from flask import make_response
from flask_restful import Resource, marshal_with, reqparse, fields
from errors import BusinessValidationError
from flask_security import auth_required
from . import course_api

course_fields = {
    "id": fields.String,
    "name": fields.String,
}

course_ratings_fields = {
    "id": fields.Integer,
    "course_id": fields.String,
    "student_id": fields.String
}

course_parser = reqparse.RequestParser()
course_parser.add_argument("id")
course_parser.add_argument("name")
course_parser.add_argument("description")
course_parser.add_argument("rating_type")
course_parser.add_argument("rating_value")
course_parser.add_argument("student_id")


class CourseApi(Resource):
    def get(self, id=None): #Get Single Course by Id or Multiple Courses
        if id is None:
            courses_required = Course.query.all()
            try:
                l = []
                for course_required in courses_required:
                    course_json = {}
                    course_json["id"] = course_required.id
                    course_json["name"] = course_required.name
                    course_json["description"] = course_required.description
                    l.append(course_json)
                return l, 200
            except AttributeError:
                return "Invalid Course ID"
        else:
            course_required = Course.query.filter_by(id=id).first()
            try:
                course_json = {}
                course_json["id"] = course_required.id
                course_json["name"] = course_required.name
                course_json["description"] = course_required.description
                return course_json, 200
            except AttributeError:
                return "Invalid Course ID"
            
class CourseRatingApi(Resource):
    @marshal_with(course_ratings_fields)
    def post(self, id): #Give Rating to a Course
        args = course_parser.parse_args()
        rating_type = args["rating_type"]
        rating_value = args["rating_value"]
        student_id = args["student_id"]
        fetched_rating = Rating.query.filter_by(type=rating_type).first()
        fetched_student = Student.query.filter_by(id=student_id).first()
        course = Course.query.filter_by(id=id).first()
        if fetched_rating is not None:
            if course is not None:
                if fetched_student is not None:
                    course_rating_record = CourseRating(
                        course_id=id,
                        student_id=student_id,
                        rating_id=fetched_rating.id,
                        value=rating_value
                    )
                    db.session.add(course_rating_record)
                    db.session.commit()
                    return course_rating_record, 201
                else:
                    raise BusinessValidationError(
                        status_code=400, error_code="S001", error_message="Student Not Found")
            else:
                raise BusinessValidationError(
                    status_code=400, error_code="C001", error_message="Course Not Found")
        else:
            raise BusinessValidationError(
                status_code=400, error_code="R001", error_message="Rating Type Not Found")

    @marshal_with(course_ratings_fields)
    def put(self, id): #Edit Rating ALready Given to a Course
        args = course_parser.parse_args()
        student_id = args["student_id"]
        rating_type = args["rating_type"]
        rating_value = args["rating_value"]
        fetched_course = Course.query.filter_by(id=id).first()
        fetched_student = Student.query.filter_by(id=student_id).first()
        fetched_rating = Rating.query.filter_by(type=rating_type).first()
        if fetched_course is not None:
            if fetched_rating is not None:
                if fetched_student is not None:
                    given_rating = CourseRating.query.filter_by(
                        student_id=student_id, course_id=id).first()
                    if given_rating is not None:
                        given_rating.value = rating_value
                        db.session.commit()
                        return given_rating
                    else:
                        raise BusinessValidationError(
                            status_code=400, error_code="CR001", error_message="Course Rating for the given Student-Course Combination Not Found")
                else:
                    raise BusinessValidationError(
                        status_code=400, error_code="S001", error_message="Student Not Found")
            else:
                raise BusinessValidationError(
                    status_code=400, error_code="R001", error_message="Rating Not Found")
        else:
            raise BusinessValidationError(
                status_code=400, error_code="C001", error_message="Course Not Found")


# class FeedbackApi(Resource):
#     @marshal_with()
#     def post(self, id):
#         pass

course_api.add_resource(CourseApi, "/api/courses/", "/api/course/<string:id>/", "/api/course/<string:id>/rating")