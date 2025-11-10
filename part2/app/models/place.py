"""
Place model for the HBnB application.
"""
import uuid
from datetime import datetime


class Place:
    """
    Place entity representing a property listing.
    """

    def __init__(self, title, description, price, latitude, longitude, owner):
        """
        Initialize a new Place.

        Args:
            title (str): Title of the place
            description (str): Description of the place
            price (float): Price per night
            latitude (float): Latitude coordinate
            longitude (float): Longitude coordinate
            owner (User): The owner of the place
        """
        self.id = str(uuid.uuid4())
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner = owner
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
        self.reviews = []  # List of reviews for this place
        self.amenities = []  # List of amenities for this place

    def validate(self):
        """
        Validate place attributes.

        Raises:
            ValueError: If validation fails
        """
        if not self.title or len(self.title.strip()) == 0:
            raise ValueError("Title is required")
        if len(self.title) > 100:
            raise ValueError("Title must not exceed 100 characters")

        if self.price is None or self.price <= 0:
            raise ValueError("Price must be a positive value")

        if self.latitude is None:
            raise ValueError("Latitude is required")
        if self.latitude < -90.0 or self.latitude > 90.0:
            raise ValueError("Latitude must be between -90.0 and 90.0")

        if self.longitude is None:
            raise ValueError("Longitude is required")
        if self.longitude < -180.0 or self.longitude > 180.0:
            raise ValueError("Longitude must be between -180.0 and 180.0")

        if not self.owner:
            raise ValueError("Owner is required")

    def update(self, data):
        """
        Update place attributes.

        Args:
            data (dict): Dictionary containing attributes to update
        """
        if 'title' in data:
            self.title = data['title']
        if 'description' in data:
            self.description = data['description']
        if 'price' in data:
            self.price = data['price']
        if 'latitude' in data:
            self.latitude = data['latitude']
        if 'longitude' in data:
            self.longitude = data['longitude']

        self.updated_at = datetime.utcnow()
        self.validate()

    def add_review(self, review):
        """Add a review to the place."""
        self.reviews.append(review)

    def add_amenity(self, amenity):
        """Add an amenity to the place."""
        if amenity not in self.amenities:
            self.amenities.append(amenity)

    def remove_amenity(self, amenity):
        """Remove an amenity from the place."""
        if amenity in self.amenities:
            self.amenities.remove(amenity)

    def to_dict(self):
        """
        Convert place to dictionary representation.

        Returns:
            dict: Dictionary representation of the place
        """
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'price': self.price,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'owner_id': self.owner.id,
            'owner': {
                'id': self.owner.id,
                'first_name': self.owner.first_name,
                'last_name': self.owner.last_name,
                'email': self.owner.email
            },
            'amenities': [amenity.to_dict() for amenity in self.amenities],
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
