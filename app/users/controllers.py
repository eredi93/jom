"""
// JOM

:copyright: (c) 2016 by Jacopo Scrinzi.
:license: MIT, see LICENSE for more details.

"""

from flask import Blueprint, abort, render_template,\
    flash, redirect, url_for, request
from flask.ext.login import login_required,\
    current_user
from functools import wraps
from app.users.models import Users
from app.users.forms import MyProfileForm, PasswordForm, RegisterForm, \
    ManageUserForm


users_mod = Blueprint('users', __name__, url_prefix='/users')


# Admin decorator
def admin_required(func):
    """If you decorate a view with this, it will ensure that the current user has
    admin privileges before calling the actual view.
    example::
        @app.route('/post')
        @login_required
        @admin_required
        def post():
            pass

    :param func: The view function to decorate.
    :type func: function
    """
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if not current_user.is_admin:
            abort(401)
        return func(*args, **kwargs)
    return decorated_view


@login_required
@users_mod.route('/', methods=('GET', ))
def index():
    """Users list

    :return: flask.render_template / flask.redirect
    """

    return render_template(
        'users/index.html',
        form=RegisterForm(),
        users=Users.select(),
        active_page='users'
    )


@login_required
@admin_required
@users_mod.route('/register', methods=('GET', 'POST'))
def register():
    """Users list

    :return: flask.render_template
    """
    form = RegisterForm()
    if form.validate_on_submit():
        Users.create_user(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data
        )
        message = '{} has been created.'.format(form.username.data)
        return render_template('modal_success.html', message=message)
    return render_template('users/register.html', form=form)


@login_required
@admin_required
@users_mod.route('/delete', methods=('GET', 'POST'))
def delete():
    """Delete user

    :return: flask.render_template
    """
    form = ManageUserForm()
    if request.method == 'GET':
        try:
            user_id = int(request.args['user'])
        except ValueError:
            return abort(500)
        user = Users.get_user(user_id)
        if not user_id or not user:
            return abort(500)
    else:
        user = Users.get_user(form.user.data)
    if form.validate_on_submit():
        if Users.delete_user(form.user.data):
            message = '{} has been deleted.'.format(user.username)
        else:
            message = 'unable to delete {}.'.format(user.username)
        return render_template('modal_success.html', message=message)
    return render_template('users/delete.html', user=user)


@login_required
@admin_required
@users_mod.route('/set-admin', methods=('GET', 'POST'))
def set_admin():
    """Users list

    :return: flask.render_template
    """
    form = ManageUserForm()
    if request.method == 'GET':
        try:
            user_id = int(request.args['user'])
        except ValueError:
            return abort(500)
        user = Users.get_user(user_id)
        if not user_id or not user:
            return abort(500)
    else:
        user = Users.get_user(form.user.data)
    if form.validate_on_submit():
        if Users.set_admin(form.user.data):
            message = '{} is now an Admin.'.format(user.username)
        else:
            message = 'unable to make Admin {}.'.format(user.username)
        return render_template('modal_success.html', message=message)
    return render_template('users/set_admin.html', user=user)


@login_required
@admin_required
@users_mod.route('/unset-admin', methods=('GET', 'POST'))
def unset_admin():
    """Users list

    :return: flask.render_template
    """
    form = ManageUserForm()
    if request.method == 'GET':
        try:
            user_id = int(request.args['user'])
        except ValueError:
            return abort(500)
        user = Users.get_user(user_id)
        if not user_id or not user:
            return abort(500)
    else:
        user = Users.get_user(form.user.data)
    if form.validate_on_submit():
        if Users.unset_admin(form.user.data):
            message = '{} is not an Admin anymore.'.format(user.username)
        else:
            message = 'unable to remove Admin privileges for {}.'.format(user.username)
        return render_template('modal_success.html', message=message)
    return render_template('users/unset_admin.html', user=user)


@login_required
@users_mod.route('/my-profile', methods=('GET', 'POST'))
def my_profile():
    """ User profile

    :return: flask.render_template / flask.redirect
    """
    form_u = MyProfileForm()
    form_pw = PasswordForm()
    if request.method == 'POST':
        if form_u.username.data == current_user.username:
            form_u.username.raw_data = None
        if form_u.email.data == current_user.email:
            form_u.email.raw_data = None
    else:
        form_u.username.data = current_user.username
        form_u.email.data = current_user.email
    if form_u.validate_on_submit():
        Users.update_user(
            user_id=current_user.id,
            username=form_u.username.data,
            email=form_u.email.data
        )
        flash('You successfully updated your profile.', 'success')
        return redirect(url_for('users.my_profile'))
    data = {
        'active_page': 'profile',
        'form_u': form_u,
        'form_pw': form_pw
    }
    return render_template('users/my_profile.html', **data)


@login_required
@users_mod.route('/my-profile/change-password', methods=('GET', 'POST'))
def change_password():
    """ User profile

    :return: flask.render_template / flask.redirect
    """
    form_u = MyProfileForm()
    form_pw = PasswordForm()
    form_u.username.data = current_user.username
    form_u.email.data = current_user.email
    if form_pw.validate_on_submit():
        old_pw = form_pw.old_password.data
        if Users.check_old_password(current_user, old_pw):
            Users.update_user(
                user_id=current_user.id,
                password=form_pw.password.data
            )
            flash('You successfully updated your password.', 'success')
            return redirect(url_for('users.my_profile'))
        else:
            form_pw.old_password.errors = ['Old password mismatch.']
            data = {
                'active_page': 'profile',
                'form_u': form_u,
                'form_pw': form_pw
            }
            return render_template('users/my_profile.html', **data)
    data = {
        'active_page': 'profile',
        'form_u': form_u,
        'form_pw': form_pw
    }
    return render_template('users/my_profile.html', **data)
