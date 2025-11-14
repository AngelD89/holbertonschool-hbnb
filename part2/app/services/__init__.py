"""
Services package initialization.
Creates a shared facade instance for all API endpoints.
"""
from app.services.facade import HBnBFacade

# Create a single shared facade instance
facade = HBnBFacade()
