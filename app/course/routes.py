# from main import *
# from course.models import *
# course_fields = {
#     "id": fields.String,
#     "name": fields.String,
#     "acronym": fields.String,
#     "credits": fields.Integer,
#     "prerequisites": fields.String,
#     "corequisites": fields.String,
#     "description": fields.String
# }

# course_parser = reqparse.RequestParser()
# course_parser.add_argument("id")
# course_parser.add_argument("name")
# course_parser.add_argument("description")

# class CourseApi(Resource):
#     def get(self, id):
#         all_courses = Course.query.filter_by(id=id).all()
#         return (all_courses)

# api.add_resource(CourseApi, "/api/courses/<id>")
