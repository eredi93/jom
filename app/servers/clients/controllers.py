"""
// JOM

:copyright: (c) 2016 by Jacopo Scrinzi.
:license: MIT, see LICENSE for more details.

"""

from flask import Blueprint, render_template, request
from flask.ext.login import login_required
from ...users.controllers import admin_required


clients_mod = Blueprint('servers', __name__,  url_prefix='/servers/clients')


@clients_mod.route('/', methods=('GET',))
@login_required
@admin_required
def certificates():
    """Servers admin page

    :return: flask.render_template
    """
    if request.args:
        print()
    return render_template(
        'servers/clients/base.html',
        active_page='certificates'
    )
