from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import ValidationError, InputRequired, Email
from .controllers import invalid_credentials, validate_username, validate_email




# This is the form used in the Login Page. It uses invalid credentials to verfiy
# username and password
class LoginForm(FlaskForm):
    username = StringField('Username',
            validators=[InputRequired(message="Username required")])
    password = PasswordField('Password',
            validators=[InputRequired(message="Password required"),
            invalid_credentials])
    submit = SubmitField('Submit')



# RegForm class is inhereting from Flask Form class for user registeration. It
# uses validate_username and validate_email functions to check if username and
# email are not in use.
class RegForm(FlaskForm):
    username = TextField('Username', validators = [validators.Length(min=4,
                    max=20,
                    message='Username should be between 4 and 20 Characters'),
                    validate_username])
    email = TextField('Email Address',
                    validators = [validators.Length(
                    min=6, max=50,message='Please enter a valid Email'),
                    Email(),
                    validate_email])
    password = PasswordField('Password', validators =[
        validators.Length(
                        min=8, message='Password length should be more than 7'),
        validators.Required(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
    # accept_tos = BooleanField('I accept the Terms of Service and Privacy' +
    #                 'Notice (updated Apr 7, 2020)',
    #                 validators = [validators.Required(
    #                 message='Please Accept the Terms and conditions.')])
    submit = SubmitField('Submit')
