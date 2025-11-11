"""
Facade pattern implementation for the HBnB application.
Provides a simplified interface to the Business Logic layer.
"""
from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity


class HBnBFacade:
    """
    Facade class to manage interactions between the API and the business logic.
    """

    def __init__(self):
        """Initialize the facade with repository instances for each entity."""
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    # User methods
    def create_user(self, user_data):
        """
        Create a new user.

        Args:
            user_data (dict): Dictionary containing user attributes

        Returns:
            User: The created user object

        Raises:
            ValueError: If validation fails or email already exists
        """
        # Check if email already exists
        existing_user = self.user_repo.get_by_attribute('email', user_data['email'])
        if existing_user:
            raise ValueError("Email already registered")

        user = User(
            first_name=user_data['first_name'],
            last_name=user_data['last_name'],
            email=user_data['email'],
            password=user_data.get('password'),
            is_admin=user_data.get('is_admin', False)
        )
        user.validate()
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        """
        Retrieve a user by ID.

        Args:
            user_id (str): The user's unique identifier

        Returns:
            User: The user object if found, None otherwise
        """
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        """
        Retrieve a user by email.

        Args:
            email (str): The user's email address

        Returns:
            User: The user object if found, None otherwise
        """
        return self.user_repo.get_by_attribute('email', email)

    def get_all_users(self):
        """
        Retrieve all users.

        Returns:
            list: List of all user objects
        """
        return self.user_repo.get_all()

    def update_user(self, user_id, user_data):
        """
        Update a user's information.

        Args:
            user_id (str): The user's unique identifier
            user_data (dict): Dictionary containing attributes to update

        Returns:
            User: The updated user object

        Raises:
            ValueError: If validation fails or email already exists for another user
        """
        user = self.get_user(user_id)
        if not user:
            return None

        # Check if email is being updated and if it already exists
        if 'email' in user_data and user_data['email'] != user.email:
            existing_user = self.user_repo.get_by_attribute('email', user_data['email'])
            if existing_user:
                raise ValueError("Email already registered")

        user.update(user_data)
        return user

    # Amenity methods
    def create_amenity(self, amenity_data):
        """
        Create a new amenity.

        Args:
            amenity_data (dict): Dictionary containing amenity attributes

        Returns:
            Amenity: The created amenity object

        Raises:
            ValueError: If validation fails or amenity name already exists
        """
        # Check if amenity name already exists
        existing_amenity = self.amenity_repo.get_by_attribute('name', amenity_data['name'])
        if existing_amenity:
            raise ValueError("Amenity name already exists")

        amenity = Amenity(name=amenity_data['name'])
        amenity.validate()
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        """
        Retrieve an amenity by ID.

        Args:
            amenity_id (str): The amenity's unique identifier

        Returns:
            Amenity: The amenity object if found, None otherwise
        """
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        """
        Retrieve all amenities.

        Returns:
            list: List of all amenity objects
        """
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        """
        Update an amenity's information.

        Args:
            amenity_id (str): The amenity's unique identifier
            amenity_data (dict): Dictionary containing attributes to update

        Returns:
            Amenity: The updated amenity object

        Raises:
            ValueError: If validation fails or name already exists for another amenity
        """
        amenity = self.get_amenity(amenity_id)
        if not amenity:
            return None

        # Check if name is being updated and if it already exists
        if 'name' in amenity_data and amenity_data['name'] != amenity.name:
            existing_amenity = self.amenity_repo.get_by_attribute('name', amenity_data['name'])
            if existing_amenity:
                raise ValueError("Amenity name already exists")

        amenity.update(amenity_data)
        return amenity

    # Place methods
    def create_place(self, place_data):
        """
        Create a new place.

        Args:
            place_data (dict): Dictionary containing place attributes

        Returns:
            Place: The created place object

        Raises:
            ValueError: If validation fails or owner doesn't exist
        """
        owner = self.get_user(place_data['owner_id'])
        if not owner:
            raise ValueError("Owner not found")

        place = Place(
            title=place_data['title'],
            description=place_data.get('description', ''),
            price=place_data['price'],
            latitude=place_data['latitude'],
            longitude=place_data['longitude'],
            owner=owner
        )
        place.validate()

        # Add amenities if provided
        if 'amenities' in place_data:
            for amenity_id in place_data['amenities']:
                amenity = self.get_amenity(amenity_id)
                if amenity:
                    place.add_amenity(amenity)

        self.place_repo.add(place)
        owner.add_place(place)
        return place

    def get_place(self, place_id):
        """
        Retrieve a place by ID.

        Args:
            place_id (str): The place's unique identifier

        Returns:
            Place: The place object if found, None otherwise
        """
        return self.place_repo.get(place_id)

    def get_all_places(self):
        """
        Retrieve all places.

        Returns:
            list: List of all place objects
        """
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        """
        Update a place's information.

        Args:
            place_id (str): The place's unique identifier
            place_data (dict): Dictionary containing attributes to update

        Returns:
            Place: The updated place object

        Raises:
            ValueError: If validation fails
        """
        place = self.get_place(place_id)
        if not place:
            return None

        # Handle amenities update if provided
        if 'amenities' in place_data:
            place.amenities = []
            for amenity_id in place_data['amenities']:
                amenity = self.get_amenity(amenity_id)
                if amenity:
                    place.add_amenity(amenity)
            del place_data['amenities']

        place.update(place_data)
        return place

    # Review methods
    def create_review(self, review_data):
        """
        Create a new review.

        Args:
            review_data (dict): Dictionary containing review attributes

        Returns:
            Review: The created review object

        Raises:
            ValueError: If validation fails or place/user doesn't exist
        """
        place = self.get_place(review_data['place_id'])
        if not place:
            raise ValueError("Place not found")

        user = self.get_user(review_data['user_id'])
        if not user:
            raise ValueError("User not found")

        review = Review(
            text=review_data['text'],
            rating=review_data['rating'],
            place=place,
            user=user
        )
        review.validate()

        self.review_repo.add(review)
        place.add_review(review)
        user.add_review(review)
        return review

    def get_review(self, review_id):
        """
        Retrieve a review by ID.

        Args:
            review_id (str): The review's unique identifier

        Returns:
            Review: The review object if found, None otherwise
        """
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        """
        Retrieve all reviews.

        Returns:
            list: List of all review objects
        """
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        """
        Retrieve all reviews for a specific place.

        Args:
            place_id (str): The place's unique identifier

        Returns:
            list: List of review objects for the place
        """
        place = self.get_place(place_id)
        if not place:
            return []
        return place.reviews

    def update_review(self, review_id, review_data):
        """
        Update a review's information.

        Args:
            review_id (str): The review's unique identifier
            review_data (dict): Dictionary containing attributes to update

        Returns:
            Review: The updated review object

        Raises:
            ValueError: If validation fails
        """
        review = self.get_review(review_id)
        if not review:
            return None

        review.update(review_data)
        return review

    def delete_review(self, review_id):
        """
        Delete a review.

        Args:
            review_id (str): The review's unique identifier

        Returns:
            bool: True if deleted, False otherwise
        """
        review = self.get_review(review_id)
        if not review:
            return False

        # Remove from place and user
        if review in review.place.reviews:
            review.place.reviews.remove(review)
        if review in review.user.reviews:
            review.user.reviews.remove(review)

        return self.review_repo.delete(review_id)
