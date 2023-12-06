from flask import Blueprint
from flask_restful import Api

course_bp = Blueprint('course', __name__)
course_api = Api(course_bp)

from . import routes