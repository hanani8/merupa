from flask import make_response
from flask_restful import HTTPException
import json
class BusinessValidationError(HTTPException):
    def __init__(self,status_code, error_code, error_message):
        message = {"Error Code": error_code, "Message": error_message}
        self.response = make_response(json.dumps(message),status_code) 