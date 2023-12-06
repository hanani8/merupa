from flask import Blueprint
from flask_restful import Api

lp_bp = Blueprint('learning_path', __name__)
lp_api = Api(lp_bp)

from . import routes