from flask.views import MethodView
from flask import jsonify, request, abort, make_response
from app.models.rides import Ride
import uuid
from app.auth.decoractor import token_required


    
class RideAPI(MethodView):
    decorators = [token_required]
    
    def __init__(self):

        if request.method != 'GET' and not request.json:
            abort(400)

    
    
    def get(self,current_user, r_id):
        """Method for  get requests"""
        if r_id:
            try:
                
                ride = Ride.find_by_id(r_id)
                if ride:
                    return jsonify(ride), 200
                return jsonify({'msg': "Ride not found "}), 404
            except Exception as e:
                response = {
                    'message': str(e)
                }
                return make_response(jsonify(response)), 500

        else:
            try:
                rides = Ride.fetch_all()
                if rides == []:
                    return jsonify({"msg": " There are no rides rides at the moment"}), 200
                return jsonify(rides), 200
            except Exception as e:
                response = {
                    'message': str(e)
                }
                return make_response(jsonify(response)), 500

    def post(self, current_user):
        """offers a new ride"""
        data = request.json

        try:

            origin = data['origin']
            destination = data['destination']
            date = data['date']
            driver = 'driver'
            ride = Ride( origin=origin, destination=destination, date=date)
            ride.insert(driver)

            response = {
                'message': 'You offered a ride successfully.',
            }
            return make_response(jsonify(response)), 201

        except Exception as e:
            response = {
                'message': str(e)
            }
            return make_response(jsonify(response)), 500
        