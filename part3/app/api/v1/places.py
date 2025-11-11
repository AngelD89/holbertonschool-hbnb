"""
Place API endpoints for the HBnB application.
"""
from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('places', description='Place operations')

# Define the amenity model for nested representation
amenity_simple_model = api.model('AmenitySimple', {
    'id': fields.String(description='Amenity ID'),
    'name': fields.String(description='Name of the amenity')
})

# Define the owner model for nested representation
owner_model = api.model('Owner', {
    'id': fields.String(description='Owner ID'),
    'first_name': fields.String(description='First name of the owner'),
    'last_name': fields.String(description='Last name of the owner'),
    'email': fields.String(description='Email of the owner')
})

# Define the place model for input validation and documentation
place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place', min_length=1, max_length=100),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night', min=0),
    'latitude': fields.Float(required=True, description='Latitude coordinate', min=-90.0, max=90.0),
    'longitude': fields.Float(required=True, description='Longitude coordinate', min=-180.0, max=180.0),
    'owner_id': fields.String(required=True, description='ID of the owner'),
    'amenities': fields.List(fields.String, description='List of amenity IDs')
})

# Define the review model for nested representation
review_simple_model = api.model('ReviewSimple', {
    'id': fields.String(description='Review ID'),
    'text': fields.String(description='Review text'),
    'rating': fields.Integer(description='Rating from 1 to 5'),
    'user_id': fields.String(description='ID of the user who wrote the review')
})

# Define the output model with nested objects
place_output_model = api.model('PlaceOutput', {
    'id': fields.String(description='Place ID'),
    'title': fields.String(description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(description='Price per night'),
    'latitude': fields.Float(description='Latitude coordinate'),
    'longitude': fields.Float(description='Longitude coordinate'),
    'owner_id': fields.String(description='Owner ID'),
    'owner': fields.Nested(owner_model, description='Owner details'),
    'amenities': fields.List(fields.Nested(amenity_simple_model), description='List of amenities'),
    'created_at': fields.String(description='Creation timestamp'),
    'updated_at': fields.String(description='Last update timestamp')
})


@api.route('/')
class PlaceList(Resource):
    """Resource for handling place collection operations."""

    @api.doc('list_places')
    @api.marshal_list_with(place_output_model)
    def get(self):
        """Retrieve a list of all places."""
        places = facade.get_all_places()
        return [place.to_dict() for place in places], 200

    @api.doc('create_place')
    @api.expect(place_model, validate=True)
    @api.marshal_with(place_output_model, code=201)
    def post(self):
        """Create a new place."""
        try:
            place_data = api.payload
            place = facade.create_place(place_data)
            return place.to_dict(), 201
        except ValueError as e:
            api.abort(400, str(e))
        except Exception as e:
            api.abort(500, f"An error occurred: {str(e)}")


@api.route('/<place_id>')
@api.param('place_id', 'The place identifier')
class PlaceResource(Resource):
    """Resource for handling individual place operations."""

    @api.doc('get_place')
    @api.marshal_with(place_output_model)
    def get(self, place_id):
        """Retrieve a place by ID."""
        place = facade.get_place(place_id)
        if not place:
            api.abort(404, "Place not found")
        return place.to_dict(), 200

    @api.doc('update_place')
    @api.expect(place_model, validate=True)
    @api.marshal_with(place_output_model)
    def put(self, place_id):
        """Update a place's information."""
        try:
            place_data = api.payload

            # Remove owner_id from update data as owner cannot be changed
            if 'owner_id' in place_data:
                del place_data['owner_id']

            place = facade.update_place(place_id, place_data)
            if not place:
                api.abort(404, "Place not found")
            return place.to_dict(), 200
        except ValueError as e:
            api.abort(400, str(e))
        except Exception as e:
            api.abort(500, f"An error occurred: {str(e)}")


@api.route('/<place_id>/reviews')
@api.param('place_id', 'The place identifier')
class PlaceReviewList(Resource):
    """Resource for retrieving reviews for a specific place."""

    @api.doc('get_place_reviews')
    @api.marshal_list_with(review_simple_model)
    def get(self, place_id):
        """Retrieve all reviews for a specific place."""
        place = facade.get_place(place_id)
        if not place:
            api.abort(404, "Place not found")

        reviews = facade.get_reviews_by_place(place_id)
        return [review.to_dict() for review in reviews], 200
