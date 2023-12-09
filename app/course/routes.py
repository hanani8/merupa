from app.course.models import *
from flask import make_response
from flask_restful import Resource, marshal_with, reqparse, fields
from app.validation import BusinessValidationError
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

course_feedback_fields = {
    "course_id": fields.String,
    "student_id": fields.String,
    "feedback": fields.String,
    "upvote": fields.Integer,
    "downvote": fields.Integer
}

course_parser = reqparse.RequestParser()
course_parser.add_argument("id")
course_parser.add_argument("name")
course_parser.add_argument("description")
course_parser.add_argument("rating_type")
course_parser.add_argument("rating_value")
course_parser.add_argument("student_id")
course_parser.add_argument("feedback")
course_parser.add_argument("vote")


class CourseApi(Resource):
    def get(self, id=None): #Get Single Course by Id or Multiple Courses
        if id is None:
            courses_required = Course.query.all()
            l = []
            for course_required in courses_required:
                course_json = {}
                course_json["id"] = course_required.id
                course_json["name"] = course_required.name
                course_json["description"] = course_required.description
                l.append(course_json)
            return l, 200
        else:
            course_required = Course.query.filter_by(id=id.upper()).first()
            try:
                course_json = {}
                course_json["id"] = course_required.id
                course_json["name"] = course_required.name
                course_json["description"] = course_required.description
                return course_json, 200
            except AttributeError:
                raise BusinessValidationError(status_code=400, error_code="C001", error_message="Course Not Found")
            
class CourseRatingApi(Resource):
    @marshal_with(course_ratings_fields)
    def post(self, id): #Give Rating to a Course
        args = course_parser.parse_args()
        rating_type = args["rating_type"]
        rating_value = args["rating_value"]
        student_id = args["student_id"]
        fetched_rating = Rating.query.filter_by(rtype=rating_type).first()
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
    def put(self, id): #Edit Rating Already Given to a Course
        args = course_parser.parse_args()
        student_id = args["student_id"]
        rating_type = args["rating_type"]
        rating_value = args["rating_value"]
        fetched_course = Course.query.filter_by(id=id).first()
        fetched_student = Student.query.filter_by(id=student_id).first()
        fetched_rating = Rating.query.filter_by(rtype=rating_type).first()
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


class CourseFeedbackApi(Resource):
    @marshal_with(course_feedback_fields)
    def post(self, id):
        args = course_parser.parse_args()
        feedback = args["feedback"]
        student_id = args["student_id"]
        fetched_student = Student.query.filter_by(id = student_id).first()
        fetched_course = Course.query.filter_by(id=id).first()
        fetched_feedback = CourseFeedback.query.filter_by(student_id = student_id, course_id = id).first()
        if fetched_feedback is None:
            if fetched_student is not None:
                if fetched_course is not None:
                    if feedback != "":
                        course_feedback_record = CourseFeedback(
                            course_id = id,
                            student_id = student_id,
                            feedback = feedback,
                            upvote = 0,
                            downvote = 0
                        )
                        db.session.add(course_feedback_record)
                        db.session.commit()
                        return course_feedback_record, 201
                    else:
                        raise BusinessValidationError(status_code=400, error_code="CF001", error_message="Empty Feedback Provided")
                else:
                    raise BusinessValidationError(status_code=400, error_code="C001", error_message="Course Not Found")
            else:
                raise BusinessValidationError(status_code=400, error_code="S001", error_message="Student Not Found")
        else:
            raise BusinessValidationError(status_code=400, error_code="CF002", error_message="Feedback Already Provided")
    
    @marshal_with(course_feedback_fields)
    def put(self, id):
        args = course_parser.parse_args()
        student_id = args["student_id"]
        vote = args.get("vote",None)
        updated_feedback = args.get("feedback",None)
        fetched_student = Student.query.filter_by(id = student_id).first()
        fetched_course = Course.query.filter_by(id = id).first()
        fetched_feedback = CourseFeedback.query.filter_by(student_id = student_id, course_id = id).first()
        if fetched_course is not None:
            if fetched_student is not None:
                if fetched_feedback is not None:
                    if (vote is None) and (updated_feedback is not None) and (updated_feedback!=""):
                        fetched_feedback.feedback = updated_feedback
                        db.session.commit()
                        return fetched_feedback, 200
                    else:
                        if vote == "upvote":
                            fetched_feedback.upvote = fetched_feedback.upvote + 1
                            db.session.commit()
                            return fetched_feedback, 200
                        elif vote == "downvote":
                            fetched_feedback.downvote = fetched_feedback.downvote + 1
                            db.session.commit()
                            return fetched_feedback, 200
                        else:
                            raise BusinessValidationError(status_code=400 , error_code="CF004", error_message="Invalid Vote Type")              
                else:
                    raise BusinessValidationError(status_code=400, error_code="CF003", error_message="No Previous Feedback to Update")
            else:
                raise BusinessValidationError(status_code=400, error_code="S001", error_message="Student Not Found")
        else:
            raise BusinessValidationError(status_code=400, error_code="C001", error_message="Course Not Found")

    def delete(self, id):
        args = course_parser.parse_args()
        student_id = args["student_id"]
        fetched_student = Student.query.filter_by(id = student_id).first()
        fetched_course = Course.query.filter_by(id = id).first()
        fetched_feedback = CourseFeedback.query.filter_by(student_id = student_id, course_id = id).first()
        if fetched_course is not None:
            if fetched_student is not None:
                if fetched_feedback is not None:
                    db.session.delete(fetched_feedback)
                    db.session.commit()
                    return "Successfully Deleted", 200
                else:
                    raise BusinessValidationError(status_code=400, error_code="CF003", error_message="No Previous Feedback to Delete")
            else:
                raise BusinessValidationError(status_code=400, error_code="S001", error_message="Student Not Found")
        else:
            raise BusinessValidationError(status_code=400, error_code="C001", error_message="Course Not Found")

course_api.add_resource(CourseApi, "/api/courses/", "/api/course/<string:id>/")
course_api.add_resource(CourseRatingApi, "/api/course/<string:id>/rating")
course_api.add_resource(CourseFeedbackApi, "/api/course/<string:id>/feedback", "/api/course/<string:id>/feedback/vote")