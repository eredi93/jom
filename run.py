"""
// JOM

:copyright: (c) 2016 by Jacopo Scrinzi.
:license: MIT, see LICENSE for more details.

"""

from app import app
from config import debug

if __name__ == '__main__':
    if debug:
        app.run(host='0.0.0.0', port=9090, debug=debug)
    else:
        app.run()
