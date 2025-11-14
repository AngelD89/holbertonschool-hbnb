"""
Authentication API endpoints for the HBnB application.
"""
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import create_access_token
from app.services import facade

api = Namespace('auth', description='Authentication operations')

# Define the login model
login_model = api.model('Login', {
    'email': fields.String(required=True, description='User email'),
    'password': fields.String(required=True, description='User password'),
})

# Define the token response model
token_model = api.model('Token', {
    'access_token': fields.String(description='JWT access token'),
})


@api.route('/login')
class Login(Resource):
    """Resource for user authentication."""

    @api.doc('login_user')
    @api.expect(login_model, validate=True)
    @api.marshal_with(token_model, code=200)
    def post(self):
        """
        Authenticate a user and return a JWT token.

        Returns:
            dict: JWT access token with user claims
        """
        credentials = api.payload
        email = credentials.get('email')
        password = credentials.get('password')

        # Get user by email
        user = facade.get_user_by_email(email)

        if not user or not user.verify_password(password):
            api.abort(401, 'Invalid credentials')

        # Create JWT token with user claims
        access_token = create_access_token(
            identity=user.id,
            additional_claims={
                'is_admin': user.is_admin,
                'email': user.email
            }
        )

        return {'access_token': access_token}, 200
