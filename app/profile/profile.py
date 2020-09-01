from flask import Blueprint, render_template, session, redirect, url_for, request
import os
from app.auth.models import users
from .models import accounts, categories
from app import db
import app.gv as gv
from flask_login import (LoginManager, login_user, current_user, logout_user,
                        login_required)
from .controllers import convertDB2DF
import pandas as pd
from app.trans.forms import StatementInput




# Blueprint Configuration
profile_bp = Blueprint('profile_bp',__name__,
                    template_folder='templates',
                    static_folder='static'
                    )




###############################################################################
#                            USER WELCOME PAGE
# This is the main page once the user login. This is customized per user.
# None logged in users cannot view this page
###############################################################################
@profile_bp.route("/welcome")
@login_required
def welcome():
    gv.user_id = current_user.id
    gv.df = convertDB2DF(current_user.id)
    gv.df['Month'] = pd.DatetimeIndex(gv.df['Date']).month
    gv.df['Year'] = pd.DatetimeIndex(gv.df['Date']).year
    gv.yearsList = list(dict.fromkeys(gv.df['Year'].tolist()))

    for y in gv.yearsList:
        gv.monDic[y] = list(dict.fromkeys(
                    gv.df[gv.df['Year']==y]['Month'].tolist()))

    categories_db = categories.query.all()
    expenseCat_db = categories.query.filter_by(type='Debit').all()
    incomeCat_db = categories.query.filter_by(type='Credit').all()
    accounts_db = accounts.query.all()

    for account in accounts_db:
        gv.accountList.append((account.id, account.account))

    for cat in expenseCat_db:
        gv.expenseCatList.append((cat.id, cat.category))

    for cat in incomeCat_db:
        gv.incomeCatList.append((cat.id, cat.category))

    return render_template("welcome.html")




###############################################################################
#                           LOGOUT PAGE
# This page handles the logout of the user
#
###############################################################################
@profile_bp.route("/logout")
@login_required
def logout():
    gv.checkpar = 0
    gv.user_id = 0
    gv.df = pd.DataFrame()
    gv.accountList = [(0,'')]
    gv.yearsList = []
    gv.monthList = []
    gv.incomeCatList=[(0,'')]
    gv.expenseCatList=[(0,'')]
    StatementInput.yearsList=[]
    current_user.authenticated = False
    current_user.is_active=False
    db.session.add(current_user)
    db.session.commit()
    session.clear()
    logout_user()
    return render_template("logout.html")
