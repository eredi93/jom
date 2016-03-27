"""
// JOM

:copyright: (c) 2016 by Jacopo Scrinzi.
:license: MIT, see LICENSE for more details.

"""

from flask import Blueprint, render_template, request, jsonify
from flask.ext.login import login_required
from app.users.controllers import admin_required
from app.servers.models import Servers
from app.servers.clients.models import Clients


clients_mod = Blueprint('clients', __name__,  url_prefix='/servers/clients')


@clients_mod.route('/', methods=('GET',))
@login_required
@admin_required
def index():
    """Servers admin page

    :return: flask.render_template
    """
    return render_template(
        'servers/clients/index.html',
        active_page='servers_clients'
    )


@clients_mod.route('/get', methods=('GET',))
@login_required
@admin_required
def get():
    """Servers admin page

    :return: flask.render_template
    """
    server = request.args.get('server')
    if not server or server not in Servers.get_servers_name():
        return jsonify({})
    aData = []
    for client in Clients.get_from_server(server):
        data = {
            'client': client.name,
            'ovpn_ip': client.ovpn_ip,
            'created_date': client.created_date,
            'revoked_date': client.revoked_date
        }
        aData.append(data)
    return jsonify({'aData': aData})