# HBnB Evolution - Part 3: Authentication, Authorization, and Database Integration

This directory contains the implementation of Part 3 of the HBnB project, which adds:
- JWT-based authentication
- Role-based authorization (user/admin)
- SQLAlchemy ORM with SQLite (dev) and MySQL (production)
- Secure password hashing with bcrypt
- Database persistence with full CRUD operations

## 🎯 Project Overview

Part 3 extends the HBnB application with enterprise-grade security and database persistence.

### Key Features Implemented

1. **User Authentication**
   - JWT token-based authentication
   - Secure password hashing with bcrypt
   - Login endpoint that issues JWT tokens
   - Token expiration (1 hour by default)

2. **Authorization & Access Control**
   - Role-based access control (regular users vs admins)
   - Ownership validation for places and reviews
   - Admin-only operations for user management and amenities
   - Public endpoints for viewing content

3. **Database Integration**
   - SQLAlchemy ORM for database operations
   - SQLite for development
   - MySQL/PostgreSQL ready for production
   - Automated schema migrations
   - Database seeding scripts

4. **Data Relationships**
   - User → Places (one-to-many)
   - User → Reviews (one-to-many)
   - Place → Reviews (one-to-many)
   - Place ↔ Amenities (many-to-many)

## 📁 Project Structure

```
part3/
├── app/
│   ├── __init__.py                    # Application factory with JWT/DB setup
│   ├── models/                        # Database models
│   ├── api/v1/                       # API endpoints
│   ├── services/                      # Business logic layer
│   └── persistence/                   # Repository layer
├── config.py                          # Configuration (dev/test/prod)
├── requirements.txt                   # Python dependencies
├── run.py                            # Application entry point
├── database_schema.sql               # SQL schema for production
├── seed_data.sql                     # Initial data (admin + amenities)
├── database_diagram.md               # ER diagram (Mermaid.js)
├── IMPLEMENTATION_GUIDE.md           # Detailed implementation guide
└── README.md                         # This file
```

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- pip (Python package manager)
- MySQL (for production) or SQLite (automatically available)

### Installation

1. **Navigate to part3 directory**
   ```bash
   cd part3
   ```

2. **Create virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set environment variables** (optional)
   ```bash
   export SECRET_KEY="your-secret-key"
   export JWT_SECRET_KEY="your-jwt-secret"
   export DATABASE_URL="sqlite:///hbnb_dev.db"
   ```

5. **Run the application**
   ```bash
   python3 run.py
   ```

The API will be available at `http://localhost:5000`

## 📚 API Documentation

See IMPLEMENTATION_GUIDE.md for detailed API documentation including:
- Authentication endpoints
- User management endpoints
- Place management endpoints
- Review endpoints
- Amenity endpoints
- Authorization requirements for each endpoint

## 🔒 Security Features

### Password Hashing
- Bcrypt with salt rounds
- Passwords never stored in plain text
- Passwords never returned in API responses

### JWT Authentication
- Tokens expire after 1 hour (configurable)
- Tokens include user ID, email, and admin status
- Protected endpoints verify JWT tokens

### Authorization Levels

1. **Public** - No authentication required
2. **Authenticated** - Valid JWT required
3. **Admin** - JWT with is_admin=true required

## 🗄️ Database Schema

See `database_diagram.md` for the complete ER diagram with:
- All entities and attributes
- Relationships between entities
- Constraints and indexes

## ✅ Completed Tasks

- [x] Task 0: Application Factory Configuration
- [x] Task 1: User Model with Password Hashing
- [x] Task 2: JWT Authentication Implementation
- [x] Task 3: Authenticated User Access Endpoints
- [x] Task 4: Administrator Access Endpoints
- [x] Task 5: SQLAlchemy Repository
- [x] Task 6: User Entity Mapping
- [x] Task 7: Place, Review, Amenity Entity Mapping
- [x] Task 8: Entity Relationship Mapping
- [x] Task 9: SQL Scripts (Schema + Seed Data)
- [x] Task 10: ER Diagram (Mermaid.js)

## 📖 Additional Resources

- **IMPLEMENTATION_GUIDE.md**: Comprehensive implementation details
- **database_diagram.md**: Visual database schema
- Flask-JWT-Extended: https://flask-jwt-extended.readthedocs.io/
- SQLAlchemy: https://docs.sqlalchemy.org/
- Flask-Bcrypt: https://flask-bcrypt.readthedocs.io/

---

**Note**: This implementation provides a solid foundation for authentication and database persistence. Review the IMPLEMENTATION_GUIDE.md for detailed information on securing endpoints and implementing full authorization logic.
