from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import *
from app import db



############################################################################
# Create USERS ORM
# |-----------|-----------|-----------|-------------|--------------|
# |    ID     | username  |   email   |  password   |authenticated |
# |-----------|-----------|-----------|-------------|--------------|
# |           |           |           |             |              |
# |-----------|-----------|-----------|-------------|--------------|
# |           |           |           |             |              |
# |-----------|-----------|-----------|-------------|--------------|
############################################################################
class users(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String, unique=True,nullable=False)
    password = db.Column(db.String,nullable=False)
    email = db.Column(db.String,nullable=False)
    authenticated = db.Column(db.Boolean, default=False)
    trans_id = db.relationship('trans', backref='user')

# The following functions are required for login_Manager
    def is_active(self):
        """True, as all users are active."""
        return True

    def get_id(self):
        """Return the user)ud to satisfy Flask-Login's requirements."""
        return self.id

    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.authenticated

    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False
