from flask import Blueprint
from flask_restful import Api

re_bp = Blueprint('learning_path', __name__)
recommendations = Api(re_bp)

from . import routes