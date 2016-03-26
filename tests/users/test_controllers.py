"""
// JOM

== Tests ==

:copyright: (c) 2016 by Jacopo Scrinzi.
:license: MIT, see LICENSE for more details.

"""

from playhouse.test_utils import test_database
from .base import ViewTestCase, TEST_DB, Users


class UsersViewsTestCase(ViewTestCase):
    """ Test Users controllers functionality """
    def create_user(self, admin=True):
        Users.create_user(
            username='root',
            email='root@example.com',
            password='password',
            admin=admin
        )

    def login(self, username, password):
        return self.app.post('/login', data=dict(
            identifier=username,
            password=password
        ))

    def edit_profile(self, username, email):
        return self.app.post('/my-profile', data=dict(
            username=username,
            email=email
        ))

    def change_password(self, password_old, password, password_confirm):
        return self.app.post('/my-profile', data=dict(
                old_password=password_old,
                password=password,
                password_confirm=password_confirm
            ))

    def register_user(self, i=""):
        data = {
            'username': 'user{}'.format(i),
            'email': 'user{}@example.com'.format(i),
            'password': 'Pa55_WorD2',
            'password_confirm': 'Pa55_WorD2'
        }
        return self.app.post('/users/register', data=data)

    def delete_user(self, id):
        data = {
            'user': id
        }
        return self.app.post('/users/delete', data=data)

    def set_user_admin(self, id):
        data = {
            'user': id
        }
        return self.app.post('/users/set-admin', data=data)

    def unset_user_admin(self, id):
        data = {
            'user': id
        }
        return self.app.post('/users/unset-admin', data=data)

    def check_admin(self):
        return self.app.post('/users/register', data=dict(user='2'))

    def test_good_login(self):
        with test_database(TEST_DB, (Users,)):
            self.create_user()
            rv = self.login('root', 'password')
            self.assertEqual(rv.status_code, 302)
            self.assertEqual(rv.location, 'http://localhost/')

    def test_bad_login(self):
        with test_database(TEST_DB, (Users,)):
            rv = self.login('root', 'password')
            self.assertEqual(rv.status_code, 200)

    def test_logout(self):
        with test_database(TEST_DB, (Users,)):
            self.create_user()
            self.login('root', 'password')
            rv = self.app.get('/logout')
            self.assertEqual(rv.status_code, 302)
            self.assertEqual(rv.location, 'http://localhost/login')

    def test_registration(self):
        with test_database(TEST_DB, (Users,)):
            self.create_user()
            self.login('root', 'password')
            rv = self.register_user()
            self.assertEqual(rv.status_code, 200)
            self.assertIn("user has been created.", rv.get_data(as_text=True).lower())

    def test_bad_registration(self):
        with test_database(TEST_DB, (Users,)):
            self.create_user()
            self.login('root', 'password')
            self.register_user()
            rv = self.register_user()
            self.assertEqual(rv.status_code, 200)
            self.assertIn("user with that name already exists.", rv.get_data(as_text=True).lower())

    def test_admin_required(self):
        with test_database(TEST_DB, (Users,)):
            self.create_user(admin=False)
            self.login('root', 'password')
            self.register_user()
            rv = self.check_admin()
            self.assertEqual(rv.status_code, 401)

    def test_my_profile(self):
        with test_database(TEST_DB, (Users,)):
            self.create_user()
            self.login('root', 'password')
            rv = self.app.get('/my-profile')
            self.assertEqual(rv.status_code, 200)
            self.assertIn("update profile" , rv.get_data(as_text=True).lower())

    def test_edit_profile(self):
        with test_database(TEST_DB, (Users,)):
            self.create_user()
            self.login('root', 'password')
            rv = self.edit_profile('root', 'foo@example.com')
            self.assertEqual(rv.status_code, 302)
            self.assertEqual(rv.location, 'http://localhost/my-profile')
            rv = self.app.get('/my-profile')
            self.assertIn("foo@example.com" , rv.get_data(as_text=True).lower())

    def test_change_password(self):
        with test_database(TEST_DB, (Users,)):
            self.create_user()
            self.login('root', 'password')
            rv = self.change_password('password', 'Pa55_WorD2', 'Pa55_WorD2')
            self.assertEqual(rv.status_code, 302)
            self.assertEqual(rv.location, 'http://localhost/my-profile')

    def test_users(self):
        with test_database(TEST_DB, (Users,)):
            self.create_user()
            self.login('root', 'password')
            self.register_user(i="1")
            self.register_user(i="2")
            rv = self.app.get('/users')
            self.assertIn("user1@example.com" , rv.get_data(as_text=True).lower())
            self.assertIn("user2@example.com" , rv.get_data(as_text=True).lower())

    def test_delete(self):
        with test_database(TEST_DB, (Users,)):
            self.create_user()
            self.login('root', 'password')
            self.register_user()
            rv = self.delete_user(id=2)
            self.assertIn("user has been deleted." , rv.get_data(as_text=True).lower())
            rv = self.app.get('/users')
            self.assertNotIn("user@example.com" , rv.get_data(as_text=True).lower())

    def test_set_admin(self):
        with test_database(TEST_DB, (Users,)):
            self.create_user()
            self.login('root', 'password')
            self.register_user()
            rv = self.set_user_admin(id=2)
            self.assertIn("user is now an admin." , rv.get_data(as_text=True).lower())

    def test_unset_admin(self):
        with test_database(TEST_DB, (Users,)):
            self.create_user()
            self.login('root', 'password')
            self.register_user()
            self.set_user_admin(id=2)
            rv = self.unset_user_admin(id=2)
            self.assertIn("user is not an admin anymore." , rv.get_data(as_text=True).lower())
