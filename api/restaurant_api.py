# restaurant_routes.py
import jwt
from flask import Blueprint, request, jsonify, g
from flask_restful import Api, Resource
from datetime import datetime
from __init__ import app
from api.jwt_authorize import token_required  # Import your JWT token decorator
from model.restaurant import Restaurant  # Your Restaurant model

# Define the Blueprint for the Restaurant API
restaurant_api = Blueprint('restaurant_api', __name__, url_prefix='/api')

# Connect the Api object to the Blueprint
api = Api(restaurant_api)

class RestaurantAPI:
    """
    Define the API CRUD endpoints for the Restaurant model.
    There are operations for creating restaurants, retrieving restaurants, and deleting restaurants.
    """

    class _CRUD(Resource):
        @token_required()  # Use token authentication for POST and DELETE routes
        def post(self):
            """
            Create a new restaurant in the system.
            """
            # Get current user from the token
            current_user = g.current_user
            # Get the request data
            data = request.get_json()

            # Validate required fields
            if not data:
                return {'message': 'No input data provided'}, 400
            if 'name' not in data or 'location' not in data or 'category' not in data or 'rating' not in data:
                return {'message': 'Name, location, category, and rating are required'}, 400

            # Create a new restaurant
            restaurant = Restaurant(
                name=data['name'],
                location=data['location'],
                category=data['category'],
                rating=data['rating'],
                user_id=current_user.id  # The user who is creating the restaurant
            )
            restaurant.create()

            return jsonify(restaurant.read()), 201

        @token_required()
        def delete(self):
            """
            Delete a specific restaurant by restaurant ID.
            Only the user who created the restaurant can delete it.
            """
            # Get current user from the token
            current_user = g.current_user
            # Get the request data
            data = request.get_json()

            # Validate required fields
            if not data or 'restaurant_id' not in data:
                return {'message': 'Restaurant ID is required'}, 400

            # Find the restaurant by ID and user
            restaurant = Restaurant.query.filter_by(id=data['restaurant_id'], user_id=current_user.id).first()
            if not restaurant:
                return {'message': 'Restaurant not found or not authorized to delete'}, 404

            # Delete the restaurant
            restaurant.delete()
            return jsonify({"message": "Restaurant removed"})

    class _GET_RESTAURANTS(Resource):
        def get(self):
            """
            Retrieve all restaurants.
            Can filter by category or location if provided.
            """
            category = request.args.get('category')
            location = request.args.get('location')

            filters = []
            if category:
                filters.append(Restaurant.category == category)
            if location:
                filters.append(Restaurant.location == location)

            # Query the database with the filters
            restaurants = Restaurant.query.filter(*filters).all() if filters else Restaurant.query.all()
            restaurants_list = [restaurant.read() for restaurant in restaurants]

            return jsonify(restaurants_list)

    """
    Map the _CRUD and _GET_RESTAURANTS classes to the API endpoints for /restaurant and /restaurant/all.
    - The _CRUD class defines the HTTP methods for creating and deleting restaurants.
    - The _GET_RESTAURANTS class defines the endpoint for retrieving all restaurants, with optional filters.
    """
    api.add_resource(_CRUD, '/restaurant')
    api.add_resource(_GET_RESTAURANTS, '/restaurant/all')
