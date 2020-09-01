from flask import Blueprint, render_template, session, redirect, url_for
from passlib.hash import pbkdf2_sha256
import os
from .forms import LoginForm, RegForm
from .models import users
from app import db
from flask_login import current_user, login_user




base_dir = os.path.dirname(os.path.dirname(__file__))
# Blueprint Configuration
auth_bp = Blueprint('auth_bp',__name__,
                    template_folder='templates',
                    static_folder='static'
                    )




###############################################################################
#                               INDEX PAGE
# Load the index page. If user is logged in, the index page will be welcome page
#
###############################################################################
@auth_bp.route('/')
def index():
    if current_user.is_active:
        return redirect(url_for('profile_bp.welcome'))
    return render_template("index.html")




###############################################################################
#                               LOGIN PAGE
# load login.html page and if username and password are correct go to welcome
# page if not reload the login page with the errors
###############################################################################
@auth_bp.route('/login', methods= ["GET","POST"])
def login():
    form= LoginForm()
    if form.validate_on_submit():
        session['username']=form.username.data
        user = users.query.filter_by(username=session['username']).first()
        user.authenticated = True
        db.session.add(user)
        db.session.commit()
        login_user(user, remember=False)
        return redirect(url_for('profile_bp.welcome'))
    else:
        return render_template("login.html",form = form)




###############################################################################
#                               SIGN UP PAGE
# load signup.html page. If everything is validated then record the data in DB
# and load signup_confirmation page. If not reload signup page with the errors
###############################################################################
@auth_bp.route('/signup', methods= ["GET","POST"])
def signup():

    form = RegForm()
    if form.validate_on_submit():
        newUser = users(username = form.username.data,
                        email = form.email.data,
                        password = pbkdf2_sha256.hash(form.password.data))
        db.session.add(newUser)
        db.session.commit()
        return redirect(url_for('auth_bp.signup_confirmation'))
    else:
        return render_template("signup.html", form = form)




###############################################################################
#                           SIGN UP CONFIRMATION PAGE
# This page displays a message to confirm the registration
#
###############################################################################
@auth_bp.route("/signup_confirmation")
def signup_confirmation():
    return render_template("signup_conf.html")
