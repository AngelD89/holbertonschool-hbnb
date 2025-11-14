"""
Review API endpoints for the HBnB application.
"""
from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('reviews', description='Review operations')

# Define the user model for nested representation
user_simple_model = api.model('UserSimple', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='First name of the user'),
    'last_name': fields.String(description='Last name of the user'),
    'email': fields.String(description='Email of the user')
})

# Define the review model for input validation and documentation
review_model = api.model('Review', {
    'text': fields.String(required=True, description='Text of the review', min_length=1),
    'rating': fields.Integer(required=True, description='Rating from 1 to 5', min=1, max=5),
    'place_id': fields.String(required=True, description='ID of the place'),
    'user_id': fields.String(required=True, description='ID of the user')
})

# Define the output model with nested objects
review_output_model = api.model('ReviewOutput', {
    'id': fields.String(description='Review ID'),
    'text': fields.String(description='Text of the review'),
    'rating': fields.Integer(description='Rating from 1 to 5'),
    'place_id': fields.String(description='Place ID'),
    'user_id': fields.String(description='User ID'),
    'user': fields.Nested(user_simple_model, description='User details'),
    'created_at': fields.String(description='Creation timestamp'),
    'updated_at': fields.String(description='Last update timestamp')
})


@api.route('/')
class ReviewList(Resource):
    """Resource for handling review collection operations."""

    @api.doc('list_reviews')
    @api.marshal_list_with(review_output_model)
    def get(self):
        """Retrieve a list of all reviews."""
        reviews = facade.get_all_reviews()
        return [review.to_dict() for review in reviews], 200

    @api.doc('create_review')
    @api.expect(review_model, validate=True)
    @api.marshal_with(review_output_model, code=201)
    def post(self):
        """Create a new review."""
        try:
            review_data = api.payload
            review = facade.create_review(review_data)
            return review.to_dict(), 201
        except ValueError as e:
            api.abort(400, str(e))
        except Exception as e:
            api.abort(500, f"An error occurred: {str(e)}")


@api.route('/<review_id>')
@api.param('review_id', 'The review identifier')
class ReviewResource(Resource):
    """Resource for handling individual review operations."""

    @api.doc('get_review')
    @api.marshal_with(review_output_model)
    def get(self, review_id):
        """Retrieve a review by ID."""
        review = facade.get_review(review_id)
        if not review:
            api.abort(404, "Review not found")
        return review.to_dict(), 200

    @api.doc('update_review')
    @api.expect(review_model, validate=True)
    @api.marshal_with(review_output_model)
    def put(self, review_id):
        """Update a review's information."""
        try:
            review_data = api.payload

            # Remove place_id and user_id from update data as they cannot be changed
            if 'place_id' in review_data:
                del review_data['place_id']
            if 'user_id' in review_data:
                del review_data['user_id']

            review = facade.update_review(review_id, review_data)
            if not review:
                api.abort(404, "Review not found")
            return review.to_dict(), 200
        except ValueError as e:
            api.abort(400, str(e))
        except Exception as e:
            api.abort(500, f"An error occurred: {str(e)}")

    @api.doc('delete_review')
    @api.response(204, 'Review deleted')
    def delete(self, review_id):
        """Delete a review."""
        success = facade.delete_review(review_id)
        if not success:
            api.abort(404, "Review not found")
        return '', 204
