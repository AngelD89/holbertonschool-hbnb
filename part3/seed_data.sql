-- HBnB Initial Data
-- This script inserts initial data including an admin user and common amenities

-- Insert admin user
-- Password is 'admin123' hashed with bcrypt
-- Note: You should generate a new bcrypt hash for production
INSERT INTO users (id, first_name, last_name, email, password, is_admin, created_at, updated_at)
VALUES (
    '36c9050e-ddd3-4c3b-9731-9f487208bbc1',
    'Admin',
    'HBnB',
    'admin@hbnb.io',
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5lW4T4EfToZVi',
    TRUE,
    NOW(),
    NOW()
);

-- Insert common amenities
INSERT INTO amenities (id, name, created_at, updated_at) VALUES
    ('a1b2c3d4-e5f6-4321-8765-111111111111', 'WiFi', NOW(), NOW()),
    ('a1b2c3d4-e5f6-4321-8765-222222222222', 'Swimming Pool', NOW(), NOW()),
    ('a1b2c3d4-e5f6-4321-8765-333333333333', 'Air Conditioning', NOW(), NOW()),
    ('a1b2c3d4-e5f6-4321-8765-444444444444', 'Kitchen', NOW(), NOW()),
    ('a1b2c3d4-e5f6-4321-8765-555555555555', 'Parking', NOW(), NOW()),
    ('a1b2c3d4-e5f6-4321-8765-666666666666', 'TV', NOW(), NOW()),
    ('a1b2c3d4-e5f6-4321-8765-777777777777', 'Gym', NOW(), NOW()),
    ('a1b2c3d4-e5f6-4321-8765-888888888888', 'Pet Friendly', NOW(), NOW()),
    ('a1b2c3d4-e5f6-4321-8765-999999999999', 'Heating', NOW(), NOW()),
    ('a1b2c3d4-e5f6-4321-8765-aaaaaaaaaaaa', 'Washer/Dryer', NOW(), NOW());

-- Verify data insertion
SELECT 'Admin user created:' AS status;
SELECT id, email, is_admin FROM users WHERE email = 'admin@hbnb.io';

SELECT 'Amenities created:' AS status;
SELECT COUNT(*) as amenity_count FROM amenities;
