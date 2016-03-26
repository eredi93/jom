"""
// JOM

:copyright: (c) 2016 by Jacopo Scrinzi.
:license: MIT, see LICENSE for more details.

"""

from flask_wtf import Form
from wtforms import StringField
from wtforms.validators import DataRequired, Regexp
from ..profiles.forms import valid_profile, server_profile_exists


class EasyRSACreateForm(Form):
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
    easy_rsa = StringField(
        'EasyRSA Location',
        validators=[
            DataRequired()
        ],
        default='/opt/jom/easyrsa/3.0'
    )
    key_size = StringField(
        'Key Size',
        validators=[
            DataRequired(),
            Regexp(
                r'^[0-9]+$',
                message="Must be an integer"
            )
        ],
        default='2048'
    )
    ca_expire = StringField(
        'CA expire',
        validators=[
            DataRequired(),
            Regexp(
                r'^[0-9]+$',
                message="Must be an integer"
            )
        ],
        default='3650'
    )
    key_expire = StringField(
        'Key expire',
        validators=[
            DataRequired(),
            Regexp(
                r'^[0-9]+$',
                message="Must be an integer"
            )
        ],
        default='3650'
    )
    country = StringField(
        'Country',
        validators=[
            DataRequired()
        ],
        default='IE'
    )
    province = StringField(
        'Province',
        validators=[
            DataRequired()
        ],
        default='DUB'
    )
    city = StringField(
        'City',
        validators=[
            DataRequired()
        ],
        default='DUB'
    )
    organization = StringField(
        'Organization',
        validators=[
            DataRequired()
        ],
        default='My cool organization'
    )
    email = StringField(
        'Email',
        validators=[
            DataRequired()
        ],
        default='email@example.com'
    )
    organizational_unit = StringField(
        'Organizational Unit',
        validators=[
            DataRequired()
        ],
        default='OpenVPN'
    )


class ManageEasyRSAForm(Form):
    """Manage profile server"""
    profile = StringField(
        'Profile',
        validators=[
            DataRequired(),
            valid_profile
        ])
