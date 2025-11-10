"""
User API endpoints for the HBnB application.
"""
from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('users', description='User operations')

# Define the user model for input validation and documentation
user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user', min_length=1, max_length=50),
    'last_name': fields.String(required=True, description='Last name of the user', min_length=1, max_length=50),
    'email': fields.String(required=True, description='Email of the user'),
})

# Define the output model (excludes password)
user_output_model = api.model('UserOutput', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='First name of the user'),
    'last_name': fields.String(description='Last name of the user'),
    'email': fields.String(description='Email of the user'),
    'is_admin': fields.Boolean(description='Admin status'),
    'created_at': fields.String(description='Creation timestamp'),
    'updated_at': fields.String(description='Last update timestamp')
})


@api.route('/')
class UserList(Resource):
    """Resource for handling user collection operations."""

    @api.doc('list_users')
    @api.marshal_list_with(user_output_model)
    def get(self):
        """Retrieve a list of all users."""
        users = facade.get_all_users()
        return [user.to_dict() for user in users], 200

    @api.doc('create_user')
    @api.expect(user_model, validate=True)
    @api.marshal_with(user_output_model, code=201)
    def post(self):
        """Create a new user."""
        try:
            user_data = api.payload
            user = facade.create_user(user_data)
            return user.to_dict(), 201
        except ValueError as e:
            api.abort(400, str(e))
        except Exception as e:
            api.abort(500, f"An error occurred: {str(e)}")


@api.route('/<user_id>')
@api.param('user_id', 'The user identifier')
class UserResource(Resource):
    """Resource for handling individual user operations."""

    @api.doc('get_user')
    @api.marshal_with(user_output_model)
    def get(self, user_id):
        """Retrieve a user by ID."""
        user = facade.get_user(user_id)
        if not user:
            api.abort(404, "User not found")
        return user.to_dict(), 200

    @api.doc('update_user')
    @api.expect(user_model, validate=True)
    @api.marshal_with(user_output_model)
    def put(self, user_id):
        """Update a user's information."""
        try:
            user_data = api.payload
            user = facade.update_user(user_id, user_data)
            if not user:
                api.abort(404, "User not found")
            return user.to_dict(), 200
        except ValueError as e:
            api.abort(400, str(e))
        except Exception as e:
            api.abort(500, f"An error occurred: {str(e)}")
