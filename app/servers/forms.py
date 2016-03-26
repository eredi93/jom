"""
// JOM

:copyright: (c) 2016 by Jacopo Scrinzi.
:license: MIT, see LICENSE for more details.

"""

from flask_wtf import Form
from wtforms import StringField, SelectField
from wtforms.validators import DataRequired, AnyOf, Regexp, ValidationError, \
    IPAddress, optional
from app.servers.models import Servers


def server_name_exists(form, field):
    """Check if server name already exists

    :param form: flask_wtf.Form
    :param field: flask_wtf.Form.field
    :return: void / wtforms.validators.ValidationError
    """
    if Servers.select().where(Servers.name == field.data).exists():
        raise ValidationError('Server with that name already exists.')


def valid_server(form, field):
    """Check if server name is valid

    :param form: flask_wtf.Form
    :param field: flask_wtf.Form.field
    :return: void / wtforms.validators.ValidationError
    """
    if not Servers.select().where(Servers.name == field.data).exists():
        raise ValidationError('Server is not recognised.')


class ServerStartStopForm(Form):
    """Server Start and Stop Form"""
    action = StringField(
        'Action',
        validators=[
            DataRequired(),
            AnyOf(
                values=['start', 'stop'],
                message='Error, accepted values are start or stop.'
            )
        ]
    )
    server_name = StringField('Server name', validators=[DataRequired()])


class ServerCreateForm(Form):
    """Server create"""
    name = StringField(
        'Name',
        validators=[
            DataRequired(),
            Regexp(
                r'^[a-zA-Z0-9_-]+$',
                message=("Server name should be one word, letters, "
                         "numbers, hyphens and underscores only.")
            ),
            server_name_exists
        ])
    server_prof = SelectField(
        'Server profile',
        validators=[
            DataRequired()
        ]
    )
    host = StringField(
        'Management Host',
        validators=[
            DataRequired(),
            IPAddress()
        ])
    port = StringField(
        'Management Port',
        validators=[
            DataRequired(),
            Regexp(
                r'^[0-9_-]+$',
                message="A number is expected."
            )
        ])
    easyrsa_prof = SelectField(
        'EasyRSA profile',
        validators=[
            DataRequired()
        ]
    )


class EditServerForm(Form):
    """Edit server"""
    pk = StringField(
        'PK',
        validators=[
            Regexp(
                r'^[a-zA-Z0-9_-]+$',
                message=("Server name should be one word, letters, "
                         "numbers, hyphens and underscores only.")
            ),
            DataRequired(),
            valid_server
        ])
    name = StringField(
        'Name',
        validators=[
            Regexp(
                r'^[a-zA-Z0-9_-]+$',
                message=("Username should be one word, letters, "
                         "numbers, hyphens and underscores only.")
            ),
            optional(),
            server_name_exists
        ])
    host = StringField(
        'Host',
        validators=[
            IPAddress(),
            optional()
        ])
    port = StringField(
        'Port',
        validators=[
            Regexp(
                r'^[0-9_-]+$',
                message="A number is expected."
            ),
            optional()
        ])


class ManageServerForm(Form):
    """Manage server"""
    server = StringField(
        'Server',
        validators=[
            DataRequired(),
            valid_server
        ])
