from flask import Blueprint
from flask_restful import Api

student_bp = Blueprint('student', __name__)
student_api = Api(student_bp)

from . import routes