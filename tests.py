from unittest import TestCase

from app import app, db
from models import User, Post, DEFAULT_IMAGE_URL

# Let's configure our app to use a different database for tests
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///blogly_test"

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()

# try separate test case for PostView
class UserViewTestCase(TestCase):
    """Test views for users."""

    def setUp(self):
        """Create test client, add sample data."""

        # As you add more models later in the exercise, you'll want to delete
        # all of their records before each test just as we're doing with the
        # User model below.
        Post.query.delete()
        User.query.delete()
        # ^ Post delete before User due to Referential Integrity

        self.client = app.test_client()

        test_user = User(
            first_name="test_first",
            last_name="test_last",
            image_url=None,
        )

        second_user = User(
            first_name="test_first_two",
            last_name="test_last_two",
            image_url=None,
        )

        db.session.add_all([test_user, second_user])
        db.session.commit()

        # We can hold onto our test_user's id by attaching it to self (which is
        # accessible throughout this test class). This way, we'll be able to
        # rely on this user in our tests without needing to know the numeric
        # value of their id, since it will change each time our tests are run.
        self.user_id = test_user.id

        test_post = Post(
            title = "test_title",
            content = "test_content",
            user_id = test_user.id,
        )

        db.session.add(test_post)
        db.session.commit()

        self.post_id = test_post.id


    def tearDown(self):
        """Clean up any fouled transaction."""
        db.session.rollback()


    def test_list_users(self):
        """Test the user page"""
        with self.client as c:

            resp = c.get("/users")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("test_first", html)
            self.assertIn("test_last", html)


    def test_create_user(self):
        """Test the add user form"""
        with self.client as c:

            test_data = {"first_name": "test_first3",
                        "last_name": "test_last3",
                        "image_url": DEFAULT_IMAGE_URL}

            resp = c.post("/users/new", data = test_data, follow_redirects=True)

            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("test_first3", html)
            self.assertIn("test_last3", html)


    def test_edit_user(self):
        """Test the edit user form"""
        with self.client as c:

            test_data = {"first_name": "test_first_edit",
                        "last_name": "test_last_edit",
                        "image_url": DEFAULT_IMAGE_URL}

            resp = c.post(
                        f"/users/{self.user_id}/edit",
                        data = test_data,
                        follow_redirects=True)

            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("test_first_edit", html)
            self.assertIn("test_last_edit", html)


    def test_delete_user(self):
        """Test the delete user button"""
        with self.client as c:

            resp = c.post(f"/users/{self.user_id}/delete", follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertNotIn("test_first_edit", html)
            self.assertNotIn("test_last_edit", html)

    def test_post_listing_for_user(self):
        """Test showing user with post lists """
        with self.client as c:

            resp = c.get(f"/users/{self.user_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("test_first", html)
            self.assertIn("test_title", html)


    def test_create_post(self):
        """Test the add post form"""
        with self.client as c:

            test_data = { "title": "test_title_3",
                        "content":"test_content_3",
                        "user_id": self.user_id}

            resp = c.post(
                        f"/users/{self.user_id}/posts/new",
                        data = test_data,
                        follow_redirects=True)

            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("test_first", html)
            self.assertIn("test_title_3", html)


    def test_edit_post(self):
        """Test the edit post form"""
        with self.client as c:

            test_data = {"title": "test_title_edit",
                        "content": "test_content_edit"}

            resp = c.post(
                        f"/posts/{self.post_id}/edit",
                        data = test_data,
                        follow_redirects=True)

            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("test_title_edit", html)
            self.assertIn("test_content_edit", html)

