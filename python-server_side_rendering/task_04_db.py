#!/usr/bin/python3
"""
Task 4: Extending Dynamic Data Display to Include SQLite in Flask
This module contains a Flask application that reads and displays product data
from JSON, CSV, or SQLite database based on query parameters.
"""

from flask import Flask, render_template, request
import json
import csv
import sqlite3

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


def read_sqlite_db(product_id=None, db_path='products.db'):
    """
    Read product data from a SQLite database.

    Args:
        product_id (int, optional): Filter by product id
        db_path (str): Path to the SQLite database

    Returns:
        list: List of product dictionaries
    """
    products = []
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        if product_id is not None:
            cursor.execute(
                'SELECT id, name, category, price FROM Products WHERE id = ?',
                (product_id,)
            )
        else:
            cursor.execute('SELECT id, name, category, price FROM Products')

        rows = cursor.fetchall()
        for row in rows:
            products.append({
                'id': row[0],
                'name': row[1],
                'category': row[2],
                'price': row[3]
            })

        conn.close()
    except (sqlite3.Error, FileNotFoundError):
        return []
    return products


@app.route('/products')
def products():
    """
    Display products from JSON, CSV, or SQLite based on source parameter.
    Supports filtering by product id.
    """
    source = request.args.get('source')
    product_id = request.args.get('id', type=int)

    # Validate source parameter
    if source not in ['json', 'csv', 'sql']:
        return render_template('product_display.html', error="Wrong source")

    # Read data from the appropriate source
    if source == 'json':
        products_list = read_json_file()
        # Filter by id if provided for JSON
        if product_id is not None:
            products_list = [p for p in products_list if p['id'] == product_id]
    elif source == 'csv':
        products_list = read_csv_file()
        # Filter by id if provided for CSV
        if product_id is not None:
            products_list = [p for p in products_list if p['id'] == product_id]
    else:  # source == 'sql'
        # For SQL, pass product_id directly to the query
        products_list = read_sqlite_db(product_id)

    # Check if product was not found
    if product_id is not None and not products_list:
        return render_template('product_display.html', error="Product not found")

    return render_template('product_display.html', products=products_list)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
