"""
// JOM

== Tests ==

:copyright: (c) 2016 by Jacopo Scrinzi.
:license: MIT, see LICENSE for more details.

"""

from unittest import TestCase
from playhouse.test_utils import test_database
from .base import TEST_DB, DoesNotExist, Users


class UserModelTestCase(TestCase):
    """ Test Users models functionality """
    def create_users(self, count=2):
        for i in range(count):
            Users.create_user(
                username='test_{}'.format(i),
                email='test_{}@example.com'.format(i),
                password='password'
            )

    def test_check_identifier(self):
        with test_database(TEST_DB, (Users,)):
            self.create_users()
            user = Users.get(username='test_1')
            self.assertEqual(Users.check_identifier(user.email), user)
            self.assertEqual(Users.check_identifier(user.username), user)

    def test_create_user(self):
        with test_database(TEST_DB, (Users,)):
            self.create_users()
            self.assertEqual(Users.select().count(), 2)
            self.assertNotEqual(
                Users.select().get().password,
                'password'
            )

    def test_create_duplicate_user(self):
        with test_database(TEST_DB, (Users,)):
            self.create_users()
            with self.assertRaises(ValueError):
                Users.create_user(
                    username='test_1',
                    email='test_1@example.com',
                    password='password'
                )

    def test_update_user(self):
        with test_database(TEST_DB, (Users,)):
            self.create_users()
            user = Users.get(username='test_1')
            user_id = user.id
            update = Users.update_user(user_id, username='user_foo', email='foo@example.com')
            self.assertEqual(update.username, 'user_foo')
            user_updated = Users.get(username='user_foo')
            self.assertEqual(user_updated.email, 'foo@example.com')

    def test_set_admin(self):
        with test_database(TEST_DB, (Users,)):
            self.create_users()
            user = Users.get(id=1)
            update = Users.set_admin(user.id)
            self.assertTrue(update.is_admin)
            user_updated = Users.get(id=1)
            self.assertTrue(user_updated.is_admin)

    def test_unset_admin(self):
        with test_database(TEST_DB, (Users,)):
            self.create_users()
            user = Users.get(id=1)
            update = Users.unset_admin(user.id)
            self.assertFalse(update.is_admin)
            user_updated = Users.get(id=1)
            self.assertFalse(user_updated.is_admin)

    def test_delete_user(self):
        with test_database(TEST_DB, (Users,)):
            self.create_users()
            user = Users.get(id=1)
            delete = Users.delete_user(user.id)
            self.assertTrue(delete)
            with self.assertRaises(DoesNotExist):
                Users.get(id=1)