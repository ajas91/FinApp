from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import *
from app import db
from app.auth.models import users
from app.profile.models import accounts, categories




############################################################################
# Create Transactions ORM
# |----|---------|------|------------|------|-------|-------------|-----------|
# | id | user_id | date | description| debit| credit| category_id | account_id|
# |----|---------|------|------------|------|-------|-------------|-----------|
# |    |         |      |    bytea   | bytea| bytea |             |           |
# |----|---------|------|------------|------|-------|-------------|-----------|
# |    |         |      |            |      |       |             |           |
# |----|---------|------|------------|------|-------|-------------|-----------|
############################################################################
class trans(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_id= db.Column(db.Integer, db.ForeignKey('users.id'))
    date = db.Column(db.DateTime, nullable=False)
    description = db.Column(db.String,nullable=False)
    debit = db.Column(db.String,nullable=False)
    credit = db.Column(db.String,nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    account_id = db.Column(db.Integer, db.ForeignKey('accounts.id'))
