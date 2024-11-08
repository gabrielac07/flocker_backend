# models/restaurant.py
from datetime import datetime
from __init__ import db
from .restaurant import Restaurant

def initRestaurants():
    # Check if the restaurants table is empty to avoid duplicate data on each run
    if db.session.query(Restaurant).count() > 0:
        print("Restaurants already initialized.")
        return

    # Sample data to populate the restaurants table
    restaurants_data = [
        {
            'name': 'Pasta Paradise',
            'location': '123 Italian St, Rome',
            'category': 'Italian',
            'rating': 4.5,
            'user_id': 1  # Assuming the user_id is 1 for the example
        },
        {
            'name': 'Sushi Central',
            'location': '456 Sushi Ave, Tokyo',
            'category': 'Japanese',
            'rating': 4.8,
            'user_id': 2  # Assuming the user_id is 2 for the example
        },
        {
            'name': 'Taco Heaven',
            'location': '789 Taco Rd, Mexico City',
            'category': 'Mexican',
            'rating': 4.2,
            'user_id': 1  # Assuming the user_id is 1 for the example
        },
        {
            'name': 'Burger Blast',
            'location': '101 Burger Blvd, New York',
            'category': 'American',
            'rating': 4.3,
            'user_id': 2  # Assuming the user_id is 2 for the example
        }
    ]

    # Loop through each restaurant data and add them to the database
    for data in restaurants_data:
        restaurant = Restaurant(
            name=data['name'],
            location=data['location'],
            category=data['category'],
            rating=data['rating'],
            user_id=data['user_id'],
            created_at=datetime.utcnow()  # Using current time for created_at
        )
        restaurant.create()  # Calling the create method from the Restaurant class to save to the DB

    print(f"Initialized {len(restaurants_data)} restaurants.")

