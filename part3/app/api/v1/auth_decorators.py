"""
Authentication and authorization decorators for protected endpoints.
"""
from functools import wraps
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request, get_jwt
from flask import abort


def jwt_required_custom(fn):
    """
    Decorator to require JWT authentication for an endpoint.
    """
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        return fn(*args, **kwargs)
    return wrapper


def admin_required(fn):
    """
    Decorator to require admin privileges for an endpoint.
    """
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt()
        if not claims.get('is_admin', False):
            abort(403, 'Admin privileges required')
        return fn(*args, **kwargs)
    return wrapper


def get_current_user_id():
    """
    Get the current user ID from the JWT token.

    Returns:
        str: User ID from JWT token
    """
    return get_jwt_identity()


def is_current_user_admin():
    """
    Check if the current user is an admin.

    Returns:
        bool: True if user is admin, False otherwise
    """
    claims = get_jwt()
    return claims.get('is_admin', False)
