# main.py
# imports from flask
import json
import os
from urllib.parse import urljoin, urlparse
from flask import abort, redirect, render_template, request, send_from_directory, url_for, jsonify  # import render_template from "public" flask libraries
from flask_login import current_user, login_user, logout_user
from flask.cli import AppGroup
from flask_login import current_user, login_required
from flask import current_app
from werkzeug.security import generate_password_hash
import shutil


# import "objects" from "this" project
from __init__ import app, db, login_manager  # Key Flask objects 
# Existing imports...
from api.pfp import pfp_api
from api.nestImg import nestImg_api  # Justin added this, custom format for his website
from api.post import post_api
from api.channel import channel_api
from api.group import group_api
from api.section import section_api
from api.nestPost import nestPost_api  # Justin added this, custom format for his website
from api.messages_api import messages_api  # Adi added this, messages for his website
from api.vote import vote_api
from api.restaurant_api import restaurant_api  # Ryan added this for the restaurant API routes

# Existing database Initialization functions
from model.user import User, initUsers
from model.section import Section, initSections
from model.group import Group, initGroups
from model.channel import Channel, initChannels
from model.post import Post, initPosts
from model.nestPost import NestPost, initNestPosts  # Justin added this, custom format for his website
from model.vote import Vote, initVotes
from model.restaurant import Restaurant, initRestaurant  # Import the restaurant model and init function

# Existing code for server only views...


# Register existing URIs for api endpoints (no changes here)
app.register_blueprint(messages_api)  # Adi added this, messages for his website
app.register_blueprint(pfp_api)
app.register_blueprint(current_user)
app.register_blueprint(post_api)
app.register_blueprint(channel_api)
app.register_blueprint(group_api)
app.register_blueprint(section_api)
app.register_blueprint(nestPost_api)
app.register_blueprint(nestImg_api)
app.register_blueprint(vote_api)
app.register_blueprint(restaurant_api)

# Rest of the code remains unchanged...
# Login manager and view functions...

# Create an AppGroup for custom commands
custom_cli = AppGroup('custom', help='Custom commands')

# Define a command to run the data generation functions
@custom_cli.command('generate_data')
def generate_data():
    # Initialize all existing models (Users, Sections, etc.)
    initUsers()
    initSections()
    initGroups()
    initChannels()
    initPosts()
    initNestPosts()
    initVotes()
    initRestaurants()  # Initialize the new Restaurant data

# Backup and restore functions remain the same...

# Define a command to backup data
@custom_cli.command('backup_data')
def backup_data():
    data = extract_data()
    save_data_to_json(data)
    backup_database(app.config['SQLALCHEMY_DATABASE_URI'], app.config['SQLALCHEMY_BACKUP_URI'])

# Define a command to restore data
@custom_cli.command('restore_data')
def restore_data_command():
    data = load_data_from_json()
    restore_data(data)

# Register the custom command group with the Flask application
app.cli.add_command(custom_cli)

# this runs the flask application on the development server
if __name__ == "__main__":
    # change name for testing
    app.run(debug=True, host="0.0.0.0", port="8887")

