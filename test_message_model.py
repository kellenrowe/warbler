import os
from unittest import TestCase
from app import app
from models import (User, Follows, Message, Like, db,
                    DEFAULT_IMAGE_URL, DEFAULT_HEADER_IMAGE_URL)
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc

bcrypt = Bcrypt()

# Make Flask errors be real errors, not HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

# disable CSRF checking for tests to work
app.config['WTF_CSRF_ENABLED'] = False

app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABASE_URL', 'postgres:///warbler-test'))

# db.drop_all()
# db.create_all()


VERY_LONG_STRING = "VERYLONGSTRINGVERYLONGVERYLONGSTRINGVERYLONGSTRINGVERYLONGVERYLONGSTRING VERY LONG STRING VERY LONG STRING VERY LONG STRING VERY LONG STRING VERY LONG STRING"
USER_IMG_URL = "https://images.theconversation.com/files/350865/original/file-20200803-24-50u91u.jpg?ixlib=rb-1.1.0&q=45&auto=format&w=1200&h=675.0&fit=crop"


class UserModelTestCase(TestCase):
    """  Tests User Model  """

    def setUp(self):
        """ Adds sample users """

        # recreates tables
        db.drop_all()
        db.create_all()

        # add user data
        user1 = User.signup("user1", "user1@user1.com", "password", None)
        user2 = User.signup("user2", "user2@user2.com",
                            "password", USER_IMG_URL)

        db.session.add(user1)
        db.session.add(user2)

        db.session.commit()

        self.user1_id = user1.id
        self.user2_id = user2.id

    def tearDown(self):
        """Rollback the data."""

        db.session.rollback()

    def test_user_repr(self):
        """ Tests that the User model __repr__ is correct """
        user1 = User.query.get(self.user1_id)

        self.assertEqual(f"{user1.__repr__}",
                         f"<bound method User.__repr__ of <User #{self.user1_id}: user1, user1@user1.com>>")

    def test_user_signup_success(self):
        """ Tests that the signup classmethod properly creates
        a user instance
        """
        user1 = User.query.get(self.user1_id)
        user2 = User.query.get(self.user2_id)

        self.assertIsInstance(user1.id, int)
        self.assertIsInstance(user2.id, int)

        self.assertEqual(user1.username, 'user1')
        self.assertEqual(user2.username, 'user2')

        self.assertEqual(user1.email, 'user1@user1.com')
        self.assertEqual(user2.email, 'user2@user2.com')

        self.assertTrue(bcrypt.check_password_hash(user1.password, 'password'))
        self.assertTrue(bcrypt.check_password_hash(user2.password, 'password'))

        self.assertEqual(user1.image_url, DEFAULT_IMAGE_URL)
        self.assertEqual(user2.image_url, USER_IMG_URL)

        self.assertEqual(user1.header_image_url, DEFAULT_HEADER_IMAGE_URL)
        self.assertEqual(user2.header_image_url, DEFAULT_HEADER_IMAGE_URL)

        self.assertEqual(user1.bio, None)
        self.assertEqual(user2.bio, None)

        self.assertEqual(user1.location, None)
        self.assertEqual(user2.location, None)

    def test_user_signup_fail_no_username(self):
        """ Tests that empty username in signup raises an error
        """

        # test that user cannot be created if username is None
        with self.assertRaises(exc.IntegrityError):
            bad_user1 = User.signup(None,
                                    "baduser1@baduser1.com",
                                    "password",
                                    None)
            db.session.add(bad_user1)
            db.session.commit()

    def test_user_signup_fail_no_email(self):
        """ Tests that empty email in signup raises an error
        """

        # test that user cannot be created if email is None
        with self.assertRaises(exc.IntegrityError):
            bad_user2 = User.signup("bad_user2",
                                    None,
                                    "password",
                                    None)
            db.session.add(bad_user2)
            db.session.commit()

    def test_user_signup_fail_no_password(self):
        """ Tests that empty password in signup raises an error
        """

        # test that user cannot be created if password is None
        with self.assertRaises(ValueError):
            bad_user3 = User.signup("bad_user3",
                                    "baduser3@baduser3.com",
                                    None,
                                    None)
            db.session.add(bad_user2)
            db.session.commit()

    def test_user_signup_fail_duplicate_username(self):
        """ Tests that a duplicate username in signup raises an error
        """

        # test that user cannot use an existing username
        with self.assertRaises(exc.IntegrityError):
            bad_user4 = User.signup("user1",
                                    "baduser4@baduser4.com",
                                    "password",
                                    None)
            db.session.add(bad_user4)
            db.session.commit()

    def test_user_signup_fail_duplicate_email(self):
        """ Tests that a duplicate email in signup raises an error
        """

        # test that user cannot use an existing email
        with self.assertRaises(exc.IntegrityError):
            bad_user5 = User.signup("bad_user5",
                                    "user1@user1.com",
                                    "password",
                                    None)
            db.session.add(bad_user5)
            db.session.commit()
