"""
// JOM

:copyright: (c) 2016 by Jacopo Scrinzi.
:license: MIT, see LICENSE for more details.

"""

import datetime
from app.database import DATABASE, Model, CharField, BooleanField, \
    PrimaryKeyField, DateTimeField, ForeignKeyField
from app.servers.models import Servers


class Clients(Model):
    """Certificates model"""
    id = PrimaryKeyField(unique=True, primary_key=True)
    name = CharField(max_length=64)
    server_id = ForeignKeyField(Servers, related_name='server')
    ovpn_ip = CharField(max_length=20)
    revoked = BooleanField(default=False)
    revoked_date = DateTimeField(default=None)
    created_date = DateTimeField(default=datetime.datetime.now)

    class Meta:
        db_table = 'clients'
        database = DATABASE
        order_by = ('name',)

    @classmethod
    def get_from_server(cls, server_id):
        return Clients.select().where(cls.server_id == server_id)