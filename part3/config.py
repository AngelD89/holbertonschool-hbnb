"""
Configuration settings for the HBnB application.
"""
import os


class Config:
    """Base configuration class."""

    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = False
    TESTING = False

    # JWT Configuration
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'jwt-secret-key-change-in-production')
    JWT_ACCESS_TOKEN_EXPIRES = 3600  # 1 hour in seconds

    # SQLAlchemy Configuration
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False


class DevelopmentConfig(Config):
    """Development configuration."""

    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        'sqlite:///hbnb_dev.db'
    )


class TestingConfig(Config):
    """Testing configuration."""

    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'


class ProductionConfig(Config):
    """Production configuration."""

    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        'mysql+pymysql://user:password@localhost/hbnb_prod'
    )


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
