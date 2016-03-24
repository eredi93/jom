"""
// JOM

:copyright: (c) 2016 by Jacopo Scrinzi.
:license: MIT, see LICENSE for more details.

"""

from peewee import *
from config import config

# Define the database object which is imported
# by modules and controllers
try:
    db_type = config['DB']['type']
except KeyError:
    db_type = None
if db_type == 'sqlite':
    DATABASE = SqliteDatabase('jom.db')
elif db_type == 'mysql':
    DATABASE = MySQLDatabase(
        config['DB']['name'],
        host=config['DB']['host'],
        user=config['DB']['user'],
        passwd=config['DB']['password']
    )
elif db_type == 'postgresql':
    DATABASE = PostgresqlDatabase(
        config['DB']['name'],
        host=config['DB']['host'],
        user=config['DB']['user'],
        passwd=config['DB']['password']
    )
else:
    DATABASE = SqliteDatabase(':memory:')