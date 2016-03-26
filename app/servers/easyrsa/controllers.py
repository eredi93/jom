"""
// JOM

:copyright: (c) 2016 by Jacopo Scrinzi.
:license: MIT, see LICENSE for more details.

"""

from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask.ext.login import login_required
from ...users.controllers import admin_required
from .models import EasyRsa
from .forms import EasyRSACreateForm, ManageEasyRSAForm


easyrsa_mod = Blueprint('servers', __name__,  url_prefix='/servers/easyrsa')


@easyrsa_mod.route('/', methods=('GET', 'POST'))
@login_required
@admin_required
def easyrsa():
    """EasyRSA profiles

    :return: flask.render_template / flask.redirect
    """
    form = EasyRSACreateForm()
    if form.validate_on_submit():
        EasyRsa.add_profile(
            profile_name=form.name.data,
            easy_rsa=form.easy_rsa.data,
            key_size=form.key_size.data,
            ca_expire=form.ca_expire.data,
            key_expire=form.key_expire.data,
            key_country=form.country.data,
            key_province=form.province.data,
            key_city=form.city.data,
            key_org=form.organization.data,
            key_email=form.email.data,
            organizational_unit=form.organizational_unit.data,
        )
        flash('EasyRSA: {} has been created.'.format(form.name.data), 'success')
        return redirect(url_for('servers.easyrsa'))
    return render_template(
        'servers/easyrsa/base.html',
        active_page='easyrsa_profiles',
        easyrsa=EasyRsa.select(),
        form=form
    )


@easyrsa_mod.route('/info', methods=('GET', 'POST'))
@login_required
@admin_required
def easyrsa_info():
    """Servers profiles

    :return: flask.render_template
    """
    profile = EasyRsa.get_profile(request.args['profile'])
    return render_template('servers/easyrsa/info.html', profile=profile)


@easyrsa_mod.route('/delete', methods=('GET', 'POST'))
@login_required
@admin_required
def easyrsa_delete():
    """Servers profiles

    :return: flask.render_template
    """
    if request.method == 'POST':
        profile = EasyRsa.get_profile(request.form.get('profile'))
    else:
        profile = EasyRsa.get_profile(request.args['profile'])
    form = ManageEasyRSAForm()
    if form.validate_on_submit():
        if EasyRsa.archive_profile(form.profile.data):
            message = '{} has been deleted.'.format(profile.name)
        else:
            message = 'unable to delete {}.'.format(profile.name)
        return render_template('modal_success.html', message=message)
    return render_template('servers/easyrsa/delete.html', profile=profile)
