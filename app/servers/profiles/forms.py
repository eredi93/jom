"""
// JOM

:copyright: (c) 2016 by Jacopo Scrinzi.
:license: MIT, see LICENSE for more details.

"""

from flask_wtf import Form
from wtforms import StringField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Regexp, AnyOf, IPAddress, \
    ValidationError
from .models import ServersProfiles


def server_profile_exists(form, field):
    """Check if server profile already exists

    :param form: flask_wtf.Form
    :param field: flask_wtf.Form.field
    :return: void / wtforms.validators.ValidationError
    """
    if ServersProfiles.select().where(ServersProfiles.name == field.data).exists():
        raise ValidationError('Server profile with that name already exists.')


def valid_profile(form, field):
    """Check if server profile id is valid

    :param form: flask_wtf.Form
    :param field: flask_wtf.Form.field
    :return: void / wtforms.validators.ValidationError
    """
    if not ServersProfiles.select().where(ServersProfiles.id == field.data).exists():
        raise ValidationError('Server is not recognised.')


class ProfileCreateForm(Form):
    """Create profile form"""
    name = StringField(
        'Profile Name',
        validators=[
            Regexp(
                r'^[a-zA-Z0-9_-]+$',
                message=("Name should be one word, letters, "
                         "numbers, hyphens and underscores only.")
            ),
            DataRequired(),
            server_profile_exists
        ]
    )
    proto = SelectField(
        'Protocol',
        validators=[
            DataRequired(),
            AnyOf(
                values=['udp', 'tcp'],
                message='Error, accepted values are udp or tcp.'
            )
        ],
        choices=[('udp', 'udp'), ('tcp', 'tcp')],
        default='udp'
    )
    port = StringField(
        'Port',
        validators=[
            Regexp(
                r'^0*(?:6553[0-5]|655[0-2][0-9]|65[0-4][0-9]{2}|6[0-4][0-9]{3}|[1-5][0-9]{4}|[1-9][0-9]{1,3}|[0-9])$',
                message="The port is not valid."
            ),
            DataRequired()
        ],
        default='1194'
    )
    dev = SelectField(
        'Dev type',
        validators=[
            DataRequired(),
            AnyOf(
                values=['tun', 'tap'],
                message='Error, accepted values are tun or tap.'
            )
        ],
        choices=[('tun', 'tun'), ('tap', 'tap')],
        default='tun'
    )
    network = StringField(
        'Network',
        validators=[
            Regexp(
                (r'^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}'
                 r'([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5]) '
                 r'(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.)'
                 r'{3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$'),
                message="Network should be 'IP Mask'->'x.x.x.x y.y.y.y'"
            ),
            DataRequired()
        ],
        default='10.8.0.0 255.255.255.0'
    )
    max_client = StringField(
        'Max Clients',
        validators=[
            Regexp(
                r'^[0-9]+$',
                message="Must be an integer"
            ),
            DataRequired()
        ],
        default='240'
    )
    mgt_host = StringField(
        'Management Host',
        validators=[
            DataRequired(),
            IPAddress()
        ],
        default='127.0.0.1'
    )
    mgt_port = StringField(
        'Management Port',
        validators=[
            Regexp(
                (r'^0*(?:6553[0-5]|655[0-2][0-9]|65[0-4][0-9]{2}|6[0-4][0-9]'
                 r'{3}|[1-5][0-9]{4}|[1-9][0-9]{1,3}|[0-9])$'),
                message="The port is not valid."
            ),
            DataRequired()
        ],
        default='7505'
    )
    extra_options = TextAreaField('Extra Options')


class ManageProfileForm(Form):
    """Manage profile server"""
    profile = StringField(
        'Profile',
        validators=[
            DataRequired(),
            valid_profile
        ])
