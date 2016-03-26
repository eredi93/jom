"""
// JOM

:copyright: (c) 2016 by Jacopo Scrinzi.
:license: MIT, see LICENSE for more details.

"""

from flask import Blueprint, render_template, flash, redirect, \
    url_for, request, jsonify
from flask.ext.login import login_required
from app.servers.forms import ServerStartStopForm, ServerCreateForm, \
    EditServerForm, ManageServerForm
from app.servers.models import Servers, ServersSupervisor
from app.servers.easyrsa.models import EasyRsa
from app.servers.profiles.models import ServersProfiles
from app.servers.supervisor.monitor import Monitor
from app.users.controllers import admin_required

servers_mod = Blueprint('servers', __name__, url_prefix='/servers')


@servers_mod.route('/', methods=('GET',))
@login_required
@admin_required
def servers():
    """Servers admin page

    :return: flask.render_template
    """
    return render_template(
        'servers/base.html',
        active_page='servers_dashboard',
        servers=Servers.select()
    )


@servers_mod.route('/start-stop', methods=('POST','GET'))
@admin_required
@login_required
def start_stop():
    """Start/stop a server

    :return: flask.redirect
    """
    form = ServerStartStopForm()
    if form.validate_on_submit():
        if form.action.data == 'stop':
            if Monitor.stop_vpn(form.server_name.data):
                Monitor.retrieve()
                flash('{} stopped successfully'.format(form.server_name.data), 'success')
                return redirect(url_for('index'))
            flash('Unable to stop {}'.format(form.server_name.data), 'error')
            return redirect(url_for('index'))
        elif form.action.data == 'start':
            if Monitor.start_vpn(form.server_name.data):
                Monitor.retrieve()
                flash('{} started successfully'.format(form.server_name.data), 'success')
                return redirect(url_for('index'))
            flash('Unable to start {}'.format(form.server_name.data), 'error')
            return redirect(url_for('index'))
        return redirect(url_for('index'))
    flash('Form validation errors: {}'.format(', '.join(form.errors)), 'error')
    return redirect(url_for('index'))


@servers_mod.route('/client-data', methods=('GET',))
@login_required
def client_data():
    """ Get client data

    :return: json
    """
    server = request.args.get('server')
    if not server or server not in Servers.get_servers_name():
        return jsonify({})
    aData = []
    for client in ServersSupervisor.select():
        data = {
            'client': client.client,
            'ovpn_ip': client.ovpn_ip,
            'public_ip': client.public_ip,
            'byte_received': client.byte_received,
            'byte_sent': client.byte_sent,
            'connected_since': client.connected_since,
            'last_ref': client.last_ref,
            'connected': client.connected,
        }
        aData.append(data)
    return jsonify({'aData': aData})


@servers_mod.route('/create', methods=('GET','POST'))
@login_required
@admin_required
def create():
    """Server add

    :return: flask.render_template
    """
    form = ServerCreateForm()
    form.server_prof.choices = [(str(s.id), s.name) for s in ServersProfiles.select()]
    form.easyrsa_prof.choices = [(str(e.id), e.name) for e in EasyRsa.select()]
    if form.validate_on_submit():
        Servers.add_server(
            name=form.name.data,
            profile_id=form.server_prof.data,
            host=form.host.data,
            port=form.port.data,
            easy_rsa_id=form.easyrsa_prof.data
        )
        message = '{} has been created.'.format(form.name.data)
        return render_template('modal_success.html', message=message)
    return render_template('servers/create.html', active_page='servers', form=form)


@servers_mod.route('/delete', methods=('GET','POST'))
@login_required
@admin_required
def delete():
    """Server delete

    :return: flask.render_template
    """
    if request.method == 'POST':
        server = Servers.get_server(request.form.get('server'))
    else:
        server = Servers.get_server(request.args['server'])
    form = ManageServerForm()
    if form.validate_on_submit():
        if Servers.archive_server(form.server.data):
            message = '{} has been deleted.'.format(server.name)
        else:
            message = 'unable to delete {}.'.format(server.name)
        return render_template('modal_success.html', message=message)
    return render_template('servers/delete.html', active_page='servers', server=server)


@servers_mod.route('/edit', methods=('GET','POST'))
@login_required
@admin_required
def edit():
    """Server edit

    :return: flask.render_template
    """
    if request.method == 'POST':
        form = EditServerForm()
        server = Servers.get_server(form.pk.data)
        if form.name.data == server.name:
            form.name.raw_data = None
        if form.host.data == server.host:
            form.host.raw_data = None
        if form.port.data == server.port:
            form.port.raw_data = None
    else:
        server = Servers.get_server(request.args['server'])
        form = EditServerForm(obj=server)
        form.pk.data = request.args['server']
    if form.validate_on_submit():
        Servers.update_server(
            pk=form.pk.data,
            name=form.name.data,
            host=form.host.data,
            port=form.port.data
        )
        message = '{} has been updated.'.format(server.name)
        return render_template('modal_success.html', message=message)
    return render_template('servers/edit.html', active_page='servers', form=form)


@servers_mod.route('/info', methods=('GET',))
@login_required
@admin_required
def info():
    """Server edit

    :return: flask.render_template
    """
    server = Servers.get_server(request.args['server'])
    return render_template('servers/info.html', server=server)
