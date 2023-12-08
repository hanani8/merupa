from flask import Blueprint
from flask_restful import Api

re_bp = Blueprint('recommendation', __name__)
recommendations = Api(re_bp)

from . import routes