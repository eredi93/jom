"""
// JOM

:copyright: (c) 2016 by Jacopo Scrinzi.
:license: MIT, see LICENSE for more details.

"""

import sys
import os
import configparser

# convert config true string to bool
def str2bool(str):
    if str.lower() in ['true', 't', 'yes', 'y']:
        return True
    elif str.lower() in ['false', 'f', 'no', 'n']:
        return False
    return str

# App mode
MODE = "development"

# Dir global var
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
APP_DIR = BASE_DIR + "/app"

# Parse config file
config = configparser.ConfigParser()
config_file = BASE_DIR + "/" + MODE + ".ini"
if os.path.isfile(config_file):
    # Read config
    config.read(config_file)
    # Set debug var
    debug = str2bool(config['APP']['DEBUG'])

# exit if config is empty
if len(config.sections()) == 0:
    print("Application config is empty or it hasn't been found.")
    sys.exit(1)