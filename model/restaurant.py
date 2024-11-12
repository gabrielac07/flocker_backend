from datetime import datetime
from sqlite3 import IntegrityError
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


class Restaurant(db.Model):
    __tablename__ = 'restaurants'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    location = db.Column(db.String(255), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    rating = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # Assuming the user who created the restaurant

    # Method to save the restaurant to the database
    def create(self):
        db.session.add(self)
        db.session.commit()

    # Method to return a JSON-serializable representation of the restaurant
    def read(self):
        return {
            'id': self.id,
            'name': self.name,
            'location': self.location,
            'category': self.category,
            'rating': self.rating,
            'created_at': self.created_at.isoformat(),
            'user_id': self.user_id
        }

    # Method to delete a restaurant from the database
    def delete(self):
        db.session.delete(self)
        db.session.commit()


# Function to initialize the restaurant table and populate it with some default restaurants
def initRestaurant():
    # Check if the restaurant table exists, create it if not
    db.create_all()

    # Example: Create some default restaurants if the table is empty
    if not Restaurant.query.first():  # Check if there are any existing restaurants in the table
        # Create some sample restaurant entries
        restaurants = [
            Restaurant(name="Pasta Palace", location="Rome, Italy", category="Italian", rating=4.7, user_id=1),
            Restaurant(name="Sushi Bar", location="Tokyo, Japan", category="Japanese", rating=4.9, user_id=2),
            Restaurant(name="Taco Haven", location="Mexico City, Mexico", category="Mexican", rating=4.5, user_id=3)
        ]
        
        # Add these restaurants to the session and commit
        db.session.add_all(restaurants)
        db.session.commit()

        print("Sample restaurants have been added to the database.")
    else:
        print("Restaurant table is already populated.")
