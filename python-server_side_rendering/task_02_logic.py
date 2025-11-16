#!/usr/bin/python3
"""
Task 2: Creating a Dynamic Template with Loops and Conditions in Flask
This module contains a Flask application that displays dynamic content
from a JSON file using Jinja's loop and conditional constructs.
"""

from flask import Flask, render_template
import json

app = Flask(__name__)


@app.route('/')
def home():
    """Render the home page."""
    return render_template('index.html')


@app.route('/about')
def about():
    """Render the about page."""
    return render_template('about.html')


@app.route('/contact')
def contact():
    """Render the contact page."""
    return render_template('contact.html')


@app.route('/items')
def items():
    """Render the items page with data from JSON file."""
    try:
        with open('items.json', 'r') as f:
            data = json.load(f)
            items_list = data.get('items', [])
    except FileNotFoundError:
        items_list = []
    except json.JSONDecodeError:
        items_list = []

    return render_template('items.html', items=items_list)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
