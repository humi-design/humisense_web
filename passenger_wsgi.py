"""
WSGI config for HUMISENSE on cPanel/Passenger.

This module exposes the WSGI application as a module-level variable named application.
"""

import sys
import os

# Add the application directory to the path
sys.path.insert(0, os.path.dirname(__file__))

# Load environment variables from .env if it exists
from dotenv import load_dotenv
env_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(env_path):
    load_dotenv(env_path)

# Import and create the Flask application
from app import app

# Application instance for Passenger
application = app
