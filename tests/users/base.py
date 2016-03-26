from app import app
from app.database import SqliteDatabase, DoesNotExist
from app.users.models import Users
from unittest import TestCase

TEST_DB = SqliteDatabase(':memory:')
TEST_DB.connect()
TEST_DB.create_tables([Users], safe=True)

class ViewTestCase(TestCase):
    """ Base View """
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        self.app = app.test_client()
