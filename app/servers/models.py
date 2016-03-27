"""models.py
DB models

created: May 2015
updated: Oct 2015

"""
import datetime
from app.database import DATABASE, Model, CharField, DateTimeField, \
    BooleanField, IntegrityError, ForeignKeyField, IntegerField
from app.servers.profiles.models import ServersProfiles, ArchiveServersProfiles
from app.servers.easyrsa.models import EasyRsa, ArchiveEasyRsa


class ServersSupervisor(Model):
    """Clients model for openvpn clients"""
    client = CharField(max_length=64, unique=True, primary_key=True)
    ovpn_ip = CharField(max_length=15, default=False)
    public_ip = CharField(max_length=22)
    byte_received = CharField(max_length=255, default=False)
    byte_sent = CharField(max_length=255, default=False)
    connected_since = CharField(max_length=64, default=False)
    last_ref = CharField(max_length=64, default=False)
    server = CharField(max_length=100)
    update_time = DateTimeField(default=datetime.datetime.now)
    connected = BooleanField(default=False)

    class Meta:
        db_table = 'servers_supervisor'
        database = DATABASE
        order_by = ('-client',)

    @classmethod
    def add_clients(cls, clients, server, update_time):
        for client in clients:
            try:
                cls.create(
                    client=client,
                    ovpn_ip=clients[client]['ovpn_ip'],
                    public_ip=clients[client]['public_ip'],
                    byte_received=clients[client]['byte_received'],
                    byte_sent=clients[client]['byte_sent'],
                    connected_since=clients[client]['connected_since'],
                    last_ref=clients[client]['last_ref'],
                    server=server,
                    update_time=update_time,
                    connected=True
                )
            except IntegrityError:
                client_record = cls.get(client=client)
                client_record.ovpn_ip = clients[client]['ovpn_ip']
                client_record.public_ip = clients[client]['public_ip']
                client_record.byte_received = clients[client]['byte_received']
                client_record.byte_sent = clients[client]['byte_sent']
                client_record.connected_since = clients[client]['connected_since']
                client_record.last_ref = clients[client]['last_ref']
                client_record.server = server
                client_record.update_time = update_time
                client_record.connected = True
                client_record.save()

    @classmethod
    def put_offline(cls):
        query = cls.update(connected=False).where(
            cls.update_time <= (datetime.datetime.now() - datetime.timedelta(minutes=2))
        )
        query.execute()


class Servers(Model):
    """Server model for openvpn servers"""
    name = CharField(max_length=64, unique=True, primary_key=True)
    profile = ForeignKeyField(ServersProfiles, related_name='server_profile')
    host = CharField(max_length=20)
    port = IntegerField()
    easy_rsa = ForeignKeyField(EasyRsa, related_name='easyrsa_profile')
    connected = IntegerField()
    status = BooleanField(default=False)
    update_time = DateTimeField()

    class Meta:
        db_table = 'servers'
        database = DATABASE
        order_by = ('name',)

    @classmethod
    def get_server(cls, name):
        return cls.get(name=name)

    @classmethod
    def add_server(cls, name, profile_id, host, port, easy_rsa_id):
        try:
            cls.create(
                name=name,
                profile=profile_id,
                host=host,
                port=port,
                easy_rsa=easy_rsa_id,
                status=0,
                connected=0,
                update_time=datetime.datetime.now()
            )
        except IntegrityError:
            raise ValueError("Server with name {} already exists".format(name))

    @classmethod
    def update_server(cls, pk, name, host, port):
        server_record = cls.get(name=pk)
        if name:
            server_record.name = name
        if host:
            server_record.host = host
        if port:
            server_record.port = port
        server_record.save()

    @classmethod
    def status_update(cls, name, status=0, connected=0):
        server_record = cls.get(name=name)
        server_record.status = status
        server_record.connected = connected
        server_record.update_time = datetime.datetime.now()
        server_record.save()

    @classmethod
    def get_servers_name(cls):
        return [server.name for server in cls.select()]

    @classmethod
    def archive_server(cls, name):
        server_record = cls.get(name=name)
        try:
            ArchiveServers.create(
                name=name,
                host=server_record.host,
                port=server_record.port,
                status=server_record.status,
                connected=server_record.connected,
                last_update_time=server_record.update_time
            )
        except IntegrityError:
            return False
        return server_record.delete_instance()


class ArchiveServers(Model):
    """Server model for openvpn servers"""
    name = CharField(unique=True, primary_key=True)
    profile = IntegerField()
    easy_rsa = IntegerField()
    last_update_time = DateTimeField(default=None)
    archived = DateTimeField(default=datetime.datetime.now)

    class Meta:
        db_table = 'archive_servers'
        database = DATABASE
        order_by = ('name',)
