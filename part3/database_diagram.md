# HBnB Database Entity-Relationship Diagram

This diagram shows the database schema for the HBnB application, including all entities and their relationships.

## Entity-Relationship Diagram

```mermaid
erDiagram
    USER ||--o{ PLACE : owns
    USER ||--o{ REVIEW : writes
    PLACE ||--o{ REVIEW : "has many"
    PLACE }o--o{ AMENITY : "includes many"

    USER {
        string id PK "Primary Key - UUID"
        string first_name "User first name (max 50 chars)"
        string last_name "User last name (max 50 chars)"
        string email UK "Unique email address (max 120 chars)"
        string password "Hashed password (bcrypt - 128 chars)"
        boolean is_admin "Admin flag (default: false)"
        datetime created_at "Creation timestamp"
        datetime updated_at "Last update timestamp"
    }

    PLACE {
        string id PK "Primary Key - UUID"
        string title "Place title (max 100 chars)"
        text description "Detailed description"
        float price "Price per night (must be positive)"
        float latitude "Latitude coordinate (-90 to 90)"
        float longitude "Longitude coordinate (-180 to 180)"
        string owner_id FK "Foreign Key to USER"
        datetime created_at "Creation timestamp"
        datetime updated_at "Last update timestamp"
    }

    REVIEW {
        string id PK "Primary Key - UUID"
        text text "Review content"
        integer rating "Rating 1-5 stars"
        string place_id FK "Foreign Key to PLACE"
        string user_id FK "Foreign Key to USER"
        datetime created_at "Creation timestamp"
        datetime updated_at "Last update timestamp"
    }

    AMENITY {
        string id PK "Primary Key - UUID"
        string name UK "Unique amenity name (max 50 chars)"
        datetime created_at "Creation timestamp"
        datetime updated_at "Last update timestamp"
    }

    PLACE_AMENITY {
        string place_id PK_FK "Composite PK - FK to PLACE"
        string amenity_id PK_FK "Composite PK - FK to AMENITY"
    }
```

## Relationship Details

### One-to-Many Relationships

1. **USER to PLACE**
   - One user can own multiple places
   - Each place belongs to exactly one owner (user)
   - Cascade delete: When a user is deleted, all their places are deleted

2. **USER to REVIEW**
   - One user can write multiple reviews
   - Each review is written by exactly one user
   - Cascade delete: When a user is deleted, all their reviews are deleted

3. **PLACE to REVIEW**
   - One place can have multiple reviews
   - Each review is for exactly one place
   - Cascade delete: When a place is deleted, all its reviews are deleted

### Many-to-Many Relationships

1. **PLACE to AMENITY** (via PLACE_AMENITY junction table)
   - One place can have multiple amenities
   - One amenity can be associated with multiple places
   - Junction table prevents duplicate associations
   - Cascade delete: When a place or amenity is deleted, the associations are removed

## Constraints and Indexes

### Unique Constraints
- `users.email`: Each email must be unique
- `amenities.name`: Each amenity name must be unique
- `reviews(user_id, place_id)`: A user can only review a place once

### Check Constraints
- `places.price > 0`: Price must be positive
- `places.latitude`: Must be between -90.0 and 90.0
- `places.longitude`: Must be between -180.0 and 180.0
- `reviews.rating`: Must be between 1 and 5

### Indexes
- `users.email`: For fast user lookup during authentication
- `places.owner_id`: For fast retrieval of places by owner
- `places(latitude, longitude)`: For geospatial queries
- `reviews.place_id`: For fast retrieval of reviews for a place
- `reviews.user_id`: For fast retrieval of reviews by a user
- `reviews.rating`: For filtering by rating

## Data Types

- **UUID (string)**: All IDs use UUID v4 format (36 characters)
- **Timestamps**: DATETIME format with automatic creation and update tracking
- **Strings**: VARCHAR with specified max lengths
- **Text**: TEXT for longer content (descriptions, review text)
- **Float**: For numeric values (price, coordinates)
- **Integer**: For discrete values (rating)
- **Boolean**: For flags (is_admin)

## Foreign Key Actions

All foreign keys use `ON DELETE CASCADE` to maintain referential integrity:
- When a user is deleted, their places and reviews are automatically deleted
- When a place is deleted, its reviews and amenity associations are automatically deleted
- When an amenity is deleted, only its associations are removed (not the places)
