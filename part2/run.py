"""
Entry point for running the HBnB Flask application.
"""
import os
from app import create_app

# Determine the configuration to use
config_name = os.getenv('FLASK_ENV', 'development')

# Create the Flask application
app = create_app(config_name)

if __name__ == '__main__':
    # Run the application
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=app.config['DEBUG']
    )
