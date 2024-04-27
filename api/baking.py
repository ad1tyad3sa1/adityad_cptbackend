# Import necessary libraries and modules
import json
import jwt
from flask import Blueprint, request, jsonify, current_app, Response
from flask_restful import Api, Resource  # Used for REST API building
from datetime import datetime
from auth_middleware import token_required

# Import the Baking model
from model.bakings import Baking

# Create a Blueprint for the baking API with a specific URL prefix
baking_api = Blueprint('baking_api', __name__, url_prefix='/api/baking')

# Initialize Flask-Restful API with the Blueprint
api = Api(baking_api)

# Define a class for handling Baking API operations
class BakingAPI:        
    # Nested class for CRUD operations on Baking resources
    class _CRUD(Resource):  
        # HTTP POST method for creating a new Baking resource
        def post(self): 
            ''' 
            Create a new Baking resource
            '''
            # Read data from the JSON request body
            body = request.get_json()
            
            # Extract recipe information from the request body
            recipe = body.get('recipe')
            
            # Create a new Baking instance with the provided recipe
            baking_object = Baking(recipe=recipe)
        
            # Attempt to create the Baking resource in the database
            baked_item = baking_object.create()
            
            # If creation is successful, return the JSON representation of the created resource
            if baked_item:
                return jsonify(baked_item.read())
            # If creation fails, return an error message
            return {'message': f'Failed to process {recipe}. Either a format error occurred or the recipe is a duplicate.'}, 400
        
        # HTTP GET method for retrieving all Baking resources
        def get(self): 
            ''' 
            Retrieve all Baking resources
            '''
            # Query all Baking resources from the database
            bakings = Baking.query.all()
            
            # Convert each Baking resource to JSON format
            json_ready = [baking.read() for baking in bakings]
            
            # Return the JSON representation of all Baking resources
            return jsonify(json_ready)
    
    # Add CRUD resource to the REST API endpoint
    api.add_resource(_CRUD, '/')