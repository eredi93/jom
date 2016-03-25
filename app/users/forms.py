"""
// JOM

:copyright: (c) 2016 by Jacopo Scrinzi.
:license: MIT, see LICENSE for more details.

"""

import re
from flask_wtf import Form
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email, Length, Regexp, \
    ValidationError, EqualTo, optional
from app.users.models import Users


def valid_identifier(form, field):
    """Cher that the identifier passed is valid

    :param form: flask_wtf.Form
    :param field: flask_wtf.Form.field
    :return: void / wtforms.validators.ValidationError
    """
    if '@' in field.data:
        regex = re.compile(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', re.IGNORECASE)
        message=('Invalid email address.')
    else:
        regex = re.compile(r'^[a-zA-Z0-9_]+$')
        message=('Invalid username.')
    match = regex.match(field.data or '')
    if not match:
        raise ValidationError(message)


def username_exists(form, field):
    """Check if username already exists

    :param form: flask_wtf.Form
    :param field: flask_wtf.Form.field
    :return: void / wtforms.validators.ValidationError
    """
    if Users.select().where(Users.username == field.data).exists():
        raise ValidationError('User with that name already exists.')


def email_exists(form, field):
    """Check if username already exists

    :param form: flask_wtf.Form
    :param field: flask_wtf.Form.field
    :return: void / wtforms.validators.ValidationError
    """
    if Users.select().where(Users.email == field.data).exists():
        raise ValidationError('Email with that name already exists.')


def valid_user(form, field):
    """Check if user id is valid

    :param form: flask_wtf.Form
    :param field: flask_wtf.Form.field
    :return: void / wtforms.validators.ValidationError
    """
    if not Users.select().where(Users.id == field.data).exists():
        raise ValidationError('User is not recognised.')


class LoginForm(Form):
    """Login form validation"""
    identifier = StringField(
        'Username/Email',
        validators=[
            DataRequired(),
            Length(min=4),
            valid_identifier
        ]
    )
    password = PasswordField('Password', validators=[DataRequired()])


class MyProfileForm(Form):
    """Edit user profile"""
    username = StringField(
        'Username',
        validators=[
            optional(),
            Regexp(
                r'^[a-zA-Z0-9_]+$',
                message=("Username should be one word, letters, "
                         "numbers, and underscores only.")
            ),
            username_exists
        ])
    email = StringField(
        'Email',
        validators=[
            optional(),
            Email(),
            email_exists
        ])


class PasswordForm(Form):
    """Change password form"""
    old_password = PasswordField(
        'Old Password',
        validators=[DataRequired()]
    )
    password = PasswordField(
        'Password',
        validators=[
            Length(min=8),
            Regexp(
                r'(?=.*[0-9].*[0-9])(?=.*[A-Z].*[A-Z])(?=.*[a-z].*[a-z].*[a-z]).*$',
                message=("Password requires 2 numbers,"
                         " 3 capital and 3 lower letters.")
            ),
            DataRequired()
        ])
    password_confirm = PasswordField(
        'Confirm Password',
        validators=[
            DataRequired(),
            EqualTo('password', message='Passwords must match')
        ]
    )


class RegisterForm(Form):
    """Registration form validation"""
    username = StringField(
        'Username',
        validators=[
            DataRequired(),
            Regexp(
                r'^[a-zA-Z0-9_]+$',
                message=("Username should be one word, letters, "
                         "numbers, and underscores only.")
            ),
            username_exists
        ])
    email = StringField(
        'Email',
        validators=[
            DataRequired(),
            Email(),
            email_exists
        ])
    password = PasswordField(
        'Password',
        validators=[
            Length(min=8),
            Regexp(
                r'(?=.*[0-9].*[0-9])(?=.*[A-Z].*[A-Z])(?=.*[a-z].*[a-z].*[a-z]).*$',
                message=("Password requires 2 numbers,"
                         " 3 capital and 3 lower letters.")
            ),
            DataRequired()
        ])
    password_confirm = PasswordField(
        'Confirm Password',
        validators=[
            DataRequired(),
            EqualTo('password', message='Passwords must match')
        ]
    )


class ManageUserForm(Form):
    """Manage user"""
    user = StringField(
        'User',
        validators=[
            DataRequired(),
            valid_user
        ])
