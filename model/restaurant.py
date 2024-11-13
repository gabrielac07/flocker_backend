from datetime import datetime
from sqlite3 import IntegrityError
from __init__ import db  # Assuming __init__.py is correctly initializing db
from model.restaurant import Restaurant

# The Restaurant class definition
class Restaurant(db.Model):
    __tablename__ = 'restaurants'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    location = db.Column(db.String(255), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    rating = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # Foreign key for user who created the restaurant

    # Constructor to initialize the Restaurant object
    def __init__(self, name, location, category, rating, user_id, created_at=None):
        """
        Constructor, 1st step in object creation.
        
        name (str): The name of the restaurant.
        location (str): The location of the restaurant.
        category (str): The type of cuisine or category the restaurant belongs to.
        rating (float): The rating of the restaurant.
        user_id (int): The user ID who created the restaurant.
        created_at (datetime, optional): Timestamp of creation (defaults to current time).
        """
        self.name = name
        self.location = location
        self.category = category
        self.rating = rating
        self.user_id = user_id
        self.created_at = created_at or datetime.utcnow()  # Use provided time or current time

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
