"""
// JOM

:copyright: (c) 2016 by Jacopo Scrinzi.
:license: MIT, see LICENSE for more details.

"""
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask.ext.login import login_required
from ...users.controllers import admin_required
from .models import ServersProfiles
from .forms import ProfileCreateForm, ManageProfileForm


profiles_mod = Blueprint('profiles', __name__,  url_prefix='/servers/profiles')


@profiles_mod.route('/', methods=('GET', 'POST'))
@login_required
@admin_required
def index():
    """Servers profiles

    :return: flask.render_template
    """
    form = ProfileCreateForm()
    if form.validate_on_submit():
        ServersProfiles.add_profile(
            name=form.name.data,
            port=form.port.data,
            dev=form.dev.data,
            network=form.network.data,
            max_client=form.max_client.data,
            mgt_host=form.mgt_host.data,
            mgt_port=form.mgt_port.data,
            extra_options=form.extra_options.data,
        )
        flash('Profile: {} has been created.'.format(form.name.data), 'success')
        return redirect(url_for('profiles.index'))
    return render_template(
        'servers/profiles/index.html',
        active_page='servers_profiles',
        profiles=ServersProfiles.select(),
        form=form
    )


@profiles_mod.route('/info', methods=('GET', 'POST'))
@login_required
@admin_required
def info():
    """Servers profiles

    :return: flask.render_template
    """
    profile = ServersProfiles.get_profile(request.args['profile'])
    return render_template('servers/profiles/info.html', profile=profile)


@profiles_mod.route('/delete', methods=('GET', 'POST'))
@login_required
@admin_required
def delete():
    """Servers profiles

    :return: flask.render_template
    """
    if request.method == 'POST':
        profile = ServersProfiles.get_profile(request.form.get('profile'))
    else:
        profile = ServersProfiles.get_profile(request.args['profile'])
    form = ManageProfileForm()
    if form.validate_on_submit():
        if ServersProfiles.archive_profile(form.profile.data):
            message = '{} has been deleted.'.format(profile.name)
        else:
            message = 'unable to delete {}.'.format(profile.name)
        return render_template('modal_success.html', message=message)
    return render_template('servers/profiles/delete.html', profile=profile)
