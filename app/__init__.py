"""
// JOM

:copyright: (c) 2016 by Jacopo Scrinzi.
:license: MIT, see LICENSE for more details.

"""

__version__ = '0.1-dev'

# import App dependencies
import re
from flask import Flask, flash, g, render_template
from flask_wtf.csrf import CsrfProtect
from config import config, str2bool
from jinja2 import evalcontextfilter, Markup, escape
from flask.ext.login import LoginManager, login_required
from flask_gravatar import Gravatar
from app.database import DATABASE
from app.logger import init_logger_models
from app.servers.models import Servers, init_servers_models
from app.servers.forms import ServerStartStopForm
from app.servers.controllers import servers_mod
from app.users.models import Users, init_users_models
from app.users.controllers import users_mod
from app.servers.profiles.controllers import profiles_mod
from app.servers.easyrsa.controllers import easyrsa_mod
from app.servers.clients.controllers import clients_mod


# init Flask app
app = Flask(__name__)
for key, val in config.items(section='APP',raw=True):
    app.config[key.upper()] = str2bool(val)
csrf = CsrfProtect(app)


# Jinja2 newline to <BR>
_paragraph_re = re.compile(r'(?:\r\n|\r|\n){2,}')


@app.template_filter()
@evalcontextfilter
def nl2br(eval_ctx, value):
    result = u'\n\n'.join(u'<p>%s</p>' % p.replace('\n', '<br>\n') \
        for p in _paragraph_re.split(escape(value)))
    if eval_ctx.autoescape:
        result = Markup(result)
    return result


# Add CSRF Handler
@csrf.error_handler
def csrf_error(reason):
    flash(reason, 'error')


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'users.login'
login_manager.login_message = ""
gravatar = Gravatar(
    app,
    size=60,
    rating='g',
    default='retro',
    force_default=False,
    use_ssl=True,
    base_url=None
)


@login_manager.user_loader
def load_user(user_id):
    """Load user

    :param user_id: string
    :return :
    """
    try:
        return Users.select().where(Users.id == int(user_id)).get()
    except Users.DoesNotExist:
        return None


@app.before_request
def before_request():
    """Connect to database before each request

    :return :
    """
    g.db = DATABASE
    g.db.connect()


@app.after_request
def after_request(response):
    """Close the database connection after each connection

    :param response:
    :return:
    """
    if hasattr(g, 'db'):
        g.db.close()
    return response


# Sample HTTP error handling
@app.errorhandler(400)
def not_found(error):
    return render_template('errors/400.html'), 400


@app.errorhandler(401)
def not_found(error):
    return render_template('errors/401.html'), 401


@app.errorhandler(404)
def not_found(error):
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def not_found(error):
    return render_template('errors/500.html'), 500


@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
    """Index view

    :return: flask.render_template / flask.redirect
    """
    servers = Servers.select()
    n_servers = servers.count()
    if n_servers != 0:
        mdl_cell = round(12 / n_servers)
    else:
        mdl_cell = 12
    data = {
        'active_page': 'index',
        'servers': servers,
        'mdl_cell': mdl_cell,
        'form': ServerStartStopForm()
    }
    return render_template('index.html', **data)


# Register blueprints
app.register_blueprint(users_mod)
app.register_blueprint(servers_mod)
app.register_blueprint(profiles_mod)
app.register_blueprint(easyrsa_mod)
app.register_blueprint(clients_mod)


# Init DB
def init_db():
    init_logger_models()
    init_users_models()
    init_servers_models()