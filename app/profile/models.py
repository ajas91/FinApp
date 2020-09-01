from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import *
from app import db




############################################################################
# Create Categories ORM
# |-------------|---------------|---------------|
# |     id      |    category   |     type      |
# |-------------|---------------|---------------|
# |             |               |               |
# |-------------|---------------|---------------|
# |             |               |               |
# |-------------|---------------|---------------|-
############################################################################
class categories(db.Model):
   id = db.Column(db.Integer, primary_key = True)
   category = db.Column(db.String,nullable=False)
   type=db.Column(db.String)
   trans_id1 = db.relationship('trans', backref='category')




############################################################################
# Create Accounts ORM
# |------------|--------------|
# |     id     |    account   |
# |------------|--------------|
# |            |              |
# |------------|--------------|
# |            |              |
# |------------|--------------|
############################################################################
class accounts(db.Model):
   id = db.Column(db.Integer, primary_key = True)
   account = db.Column(db.String, nullable=False)
   trans_id2 = db.relationship('trans', backref='account')
