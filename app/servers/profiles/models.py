"""
// JOM

:copyright: (c) 2016 by Jacopo Scrinzi.
:license: MIT, see LICENSE for more details.

"""

import datetime
from app.database import DATABASE, Model, CharField, IntegrityError, \
    PrimaryKeyField, IntegerField, TextField, DateTimeField


class ServersProfiles(Model):
    """Server model for openvpn servers"""
    id = PrimaryKeyField(unique=True, primary_key=True)
    name = CharField(max_length=64, unique=True)
    proto = CharField(max_length=3, default='udp')
    port = IntegerField(default=1194)
    dev = CharField(max_length=3, default='tun')
    network = CharField(default="10.8.0.0 255.255.255.0")
    max_client = IntegerField(default=240)
    mgt_host = CharField(max_length=15, default="127.0.0.1")
    mgt_port = IntegerField(default=7505)
    extra_options = TextField()

    class Meta:
        db_table = 'servers_profiles'
        database = DATABASE
        order_by = ('name',)

    @classmethod
    def get_profile(cls, profile_id):
        return cls.get(id=profile_id)

    @classmethod
    def add_profile(cls, name, port, dev, network, max_client, mgt_host,
                    mgt_port, extra_options=None):
        cls.create(
            name=name,
            port=port,
            dev=dev,
            network=network,
            max_client=max_client,
            mgt_host=mgt_host,
            mgt_port=mgt_port,
            extra_options=extra_options
        )

    def archive_profile(self):
        if not self.name:
            raise ValueError(
                "Trying to archive empty object"
            )
        try:
            ArchiveServersProfiles.create(
                profile_id=self.id,
                name=self.name,
                port=self.port,
                dev=self.dev,
                network=self.network,
                max_client=self.max_client,
                mgt_host=self.mgt_host,
                mgt_port=self.mgt_port,
                extra_options=self.extra_options
            )
        except IntegrityError:
            raise ValueError(
                "Server Profile with name {} already archived".format(self.name)
            )
        return self.delete_instance()


class ArchiveServersProfiles(Model):
    """Server model for openvpn servers"""
    id = PrimaryKeyField(unique=True, primary_key=True)
    profile_id = IntegerField()
    name = CharField()
    port = IntegerField()
    dev = CharField()
    network = CharField()
    max_client = IntegerField()
    mgt_host = CharField()
    mgt_port = IntegerField()
    extra_options = TextField()
    archived = DateTimeField(default=datetime.datetime.now)

    class Meta:
        db_table = 'archive_servers_profiles'
        database = DATABASE
        order_by = ('name',)
