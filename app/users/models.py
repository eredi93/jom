"""
// JOM

:copyright: (c) 2016 by Jacopo Scrinzi.
:license: MIT, see LICENSE for more details.

"""

from flask.ext.login import UserMixin
from flask.ext.bcrypt import generate_password_hash, check_password_hash
from app.database import DATABASE, Model, CharField, BooleanField, IntegrityError


class Users(UserMixin, Model):
    """User model for app users"""
    username = CharField(unique=True)
    email = CharField(unique=True)
    password = CharField(max_length=100)
    is_admin = BooleanField(default=False)

    class Meta:
        db_table = 'users'
        database = DATABASE

    @classmethod
    def get_user(cls, user_id):
        try:
            user = cls.get(id=user_id)
        except cls.DoesNotExist:
            return False
        return user

    @classmethod
    def check_identifier(cls, identifier):
        if '@' in identifier:
            try:
                user = cls.get(cls.email == identifier)
            except cls.DoesNotExist:
                return False
        else:
            try:
                user = cls.get(cls.username == identifier)
            except cls.DoesNotExist:
                return False
        return user

    @classmethod
    def check_old_password(cls, user, old_password):
        return check_password_hash(user.password, old_password)

    @classmethod
    def create_user(cls, username, email, password, admin=False):
        try:
            user_record = cls.create(username=username,
                       email=email,
                       password=generate_password_hash(password),
                       is_admin=admin)
        except IntegrityError:
            raise ValueError("User already exists")
        return user_record

    @classmethod
    def update_user(cls, user_id, username=None, email=None, password=None):
        user_record = cls.get(id=user_id)
        if username:
            user_record.username = username
        if email:
            user_record.email = email
        if password:
            user_record.password = generate_password_hash(password)
        user_record.save()
        return user_record

    @classmethod
    def set_admin(cls, user_id):
        user_record = cls.get(id=user_id)
        user_record.is_admin = True
        user_record.save()
        return user_record

    @classmethod
    def unset_admin(cls, user_id):
        user_record = cls.get(id=user_id)
        user_record.is_admin = False
        user_record.save()
        return user_record

    @classmethod
    def delete_user(cls, user_id):
        user_record = cls.delete().where(cls.id == user_id)
        return user_record.execute()
