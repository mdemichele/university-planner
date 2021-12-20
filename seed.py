"""Seed File"""

from models import User, Course, db 
from app import app 

# Create all tables 
db.drop_all()
db.create_all()

# If table isn't empty, empty it 
User.query.delete()

