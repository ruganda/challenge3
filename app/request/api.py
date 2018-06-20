from flask.views import MethodView
from flask import jsonify, request, abort, make_response
from app.models import Request
import uuid
from app.auth.decoractor import token_required

class RequestAPI(MethodView):
    """This class-based view for requesting a ride."""
    decorators = [token_required]
    def post(self,current_user, ride_id):
        if ride_id:
            try:
                passenger = current_user.username
                Request.insert(ride_id, passenger)  
                return jsonify({'msg': 'A request to join this ride has been sent' }), 201 
                
            except Exception as e:
                response = {
                    'message': str(e)
                }
                return make_response(jsonify(response)), 500
