"""
// JOM

:copyright: (c) 2016 by Jacopo Scrinzi.
:license: MIT, see LICENSE for more details.

"""
__version__ = '0.1'

# import App dependencies
import re
from flask import Flask, flash
from flask_wtf.csrf import CsrfProtect
from config import config, str2bool
from jinja2 import evalcontextfilter, Markup, escape

#init Flask app
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