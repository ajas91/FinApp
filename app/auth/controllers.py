from passlib.hash import pbkdf2_sha256
from .models import users
from wtforms.validators import ValidationError



# This function checks the user credentials once user input username
# and password. It is used in LoginForm
def invalid_credentials(form, field):
    """ Username and password checker """
    password = field.data
    username = form.username.data
    # Check username is invalid
    user_data = users.query.filter_by(username=username).first()
    if user_data is None:
        raise ValidationError("Username or password is incorrect")
    # Check password in invalid
    elif not pbkdf2_sha256.verify(password, user_data.password):
        raise ValidationError("Username or password is incorrect")




# This function is used in to validate if username is already in use during
# registeration and returns a message if so.
def validate_username(form,field):
    """Username usage checker"""
    if len(users.query.filter_by(username=field.data).all()) != 0:
        raise ValidationError("Username Already exist!"
            + "Choose different user")




# This function is used in to validate if email is already in use during
# registeration and returns a message if so.
def validate_email(form,field):
    """email usage checker"""
    if (users.query.filter_by(email=field.data).first()) is not None:
        raise ValidationError("Email is already in use!")
