#!/usr/bin/python3
"""
Task 3: Displaying Data from JSON or CSV Files in Flask
This module contains a Flask application that reads and displays product data
from JSON or CSV files based on query parameters.
"""

from flask import Flask, render_template, request
import json
import csv

app = Flask(__name__)


def read_json_file(filepath='products.json'):
    """
    Read product data from a JSON file.

    Args:
        filepath (str): Path to the JSON file

    Returns:
        list: List of product dictionaries
    """
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def read_csv_file(filepath='products.csv'):
    """
    Read product data from a CSV file.

    Args:
        filepath (str): Path to the CSV file

    Returns:
        list: List of product dictionaries
    """
    products = []
    try:
        with open(filepath, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Convert id to int and price to float
                products.append({
                    'id': int(row['id']),
                    'name': row['name'],
                    'category': row['category'],
                    'price': float(row['price'])
                })
    except (FileNotFoundError, ValueError, KeyError):
        return []
    return products


@app.route('/products')
def products():
    """
    Display products from JSON or CSV file based on source parameter.
    Supports filtering by product id.
    """
    source = request.args.get('source')
    product_id = request.args.get('id', type=int)

    # Validate source parameter
    if source not in ['json', 'csv']:
        return render_template('product_display.html', error="Wrong source")

    # Read data from the appropriate source
    if source == 'json':
        products_list = read_json_file()
    else:  # source == 'csv'
        products_list = read_csv_file()

    # Filter by id if provided
    if product_id is not None:
        filtered_products = [p for p in products_list if p['id'] == product_id]
        if not filtered_products:
            return render_template('product_display.html', error="Product not found")
        products_list = filtered_products

    return render_template('product_display.html', products=products_list)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
