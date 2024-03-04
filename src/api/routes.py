"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User
from api.utils import generate_sitemap, APIException
from flask_cors import CORS

from flask_jwt_extended import create_access_token
from flask_jwt_extended import jwt_required
from flask_jwt_extended import get_jwt_identity

api = Blueprint('api', __name__)


# Allow CORS requests to this API
CORS(api)

@api.route('/hello', methods=['POST', 'GET'])
def handle_hello():

    response_body = {
        "message": "Hello! I'm a message that came from the backend, check the network tab on the google inspector and you will see the GET request"
    }

    return jsonify(response_body), 200


# Create a route to authenticate your users and return JWTs. The
# create_access_token() function is used to actually generate the JWT.
@api.route("/token", methods=["POST"])
def handle_token():
    email = request.json.get("email", None)
    password = request.json.get("password", None)

    print("EMAIL!!!!!!")
    print(email)

    print("Password!!!!!!!!")
    print(password)

    user = User.query.filter_by(email=email).one_or_none()

    print("USER!!!!!!!")
    print(user)

    if not user or not user.check_password(password):
        return jsonify("Wrong email or password"), 401

    access_token = create_access_token(identity=user.token_serialize())
    return jsonify(access_token=access_token)


@api.route("/me", methods=["GET"])
@jwt_required()
def manage_profile():
    identity = get_jwt_identity()
    print("IDENTITY")
    current_user = User.query.filter_by(id=identity["id"]).one_or_none()
    
    return jsonify(current_user.serialize())