"""
// JOM

:copyright: (c) 2016 by Jacopo Scrinzi.
:license: MIT, see LICENSE for more details.

"""

import datetime
from app.database import DATABASE, Model, CharField, IntegrityError, \
    PrimaryKeyField, IntegerField, DateTimeField


class EasyRsa(Model):
    id = PrimaryKeyField()
    profile_name = CharField(unique=True)
    easy_rsa = CharField(default="/opt/jom/easyrsa/3.0")
    key_size = IntegerField(default=2048)
    ca_expire = IntegerField(default=3650)
    key_expire = IntegerField(default=3650)
    country = CharField(default="IE")
    province = CharField(default="DUB")
    city = CharField(default="Dublin")
    organization = CharField(default="My cool organization")
    email = CharField(default="email@example.com")
    organizational_unit = CharField(default="OpenVPN")

    class Meta:
        db_table = 'easy_rsa'
        database = DATABASE
        order_by = ('profile_name',)

    @classmethod
    def get_profile(cls, profile_id):
        return cls.get(id=profile_id)

    @classmethod
    def add_profile(cls, profile_name, easy_rsa, key_size, ca_expire,
                    key_expire, key_country, key_province, key_city,
                    key_org, key_email, organizational_unit):
        cls.create(
            profile_name=profile_name,
            EASY_RSA=easy_rsa,
            KEY_SIZE=key_size,
            CA_EXPIRE=ca_expire,
            KEY_EXPIRE=key_expire,
            KEY_COUNTRY=key_country,
            KEY_PROVINCE=key_province,
            KEY_CITY=key_city,
            KEY_ORG=key_org,
            KEY_EMAIL=key_email,
            KEY_NAME=organizational_unit,
        )

    def archive_profile(self):
        if not self.name:
            raise ValueError(
                "Trying to archive empty object"
            )
        try:
            ArchiveEasyRsa.create(
                profile_id=self.id,
                profile_name=self.profile_name,
                EASY_RSA=self.EASY_RSA,
                KEY_SIZE=self.KEY_SIZE,
                CA_EXPIRE=self.CA_EXPIRE,
                KEY_EXPIRE=self.KEY_EXPIRE,
                KEY_COUNTRY=self.KEY_COUNTRY,
                KEY_PROVINCE=self.KEY_PROVINCE,
                KEY_CITY=self.KEY_CITY,
                KEY_ORG=self.KEY_ORG,
                KEY_EMAIL=self.KEY_EMAIL,
                KEY_NAME=self.KEY_NAME
            )
        except IntegrityError:
            raise ValueError(
                "EasyRsa with name {} already archived".format(self.name)
            )
        return self.delete_instance()


class ArchiveEasyRsa(Model):
    id = PrimaryKeyField()
    profile_id = IntegerField()
    profile_name = CharField(unique=True)
    EASY_RSA = CharField()
    KEY_SIZE = IntegerField()
    CA_EXPIRE = IntegerField()
    KEY_EXPIRE = IntegerField()
    KEY_COUNTRY = CharField()
    KEY_PROVINCE = CharField()
    KEY_CITY = CharField()
    KEY_ORG = CharField()
    KEY_EMAIL = CharField()
    KEY_OU = CharField()
    KEY_NAME = CharField()
    archived = DateTimeField(default=datetime.datetime.now)

    class Meta:
        db_table = 'archive_easy_rsa'
        database = DATABASE
        order_by = ('profile_name',)
