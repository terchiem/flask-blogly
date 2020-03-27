from unittest import TestCase
from app import app
from models import User, db

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False
app.config['TESTING'] = True
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()

class UserTestCase(TestCase):
    """ Tests for users class """

    def setUp(self):
        """ Add sample user """

        db.session.rollback()
        User.query.delete()

        user = User(first_name="Test", last_name="User")
        user2 = User(first_name="Test2", last_name="User2")
        db.session.add(user)
        db.session.add(user2)
        db.session.commit()

        self.user_id = user.id

    def tearDown(self):
        """ Clean up any fouled transaction. """

        db.session.rollback()

    def test_get_user_list(self):
        """ Test user list page """

        with app.test_client() as client:
            resp = client.get("/users")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('id="user-list-id"', html)
            self.assertIn('Test User', html) 


    def test_add_user(self):
        """ Test creating a new user """

        with app.test_client() as client:
            d = {"first_name": "Bob", "last_name": "Smith" }
            resp = client.post("/users/new", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Bob Smith', html)
            self.assertIn(f'<a href="/users/{self.user_id}">', html)
            self.assertIn(f'<a href="/users/{self.user_id + 2}">', html)


    def test_edit_user(self):
        """ Test editing a user """

        with app.test_client() as client:
            d = {"first_name": "Jane", "last_name": "Smith" }
            resp = client.post(f"/users/{self.user_id}/edit", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Jane Smith', html)
            self.assertIn(f'<a href="/users/{self.user_id}">', html)
    
    def test_empty_edit_user(self):
        """ Test editing a user """

        with app.test_client() as client:
            resp = client.post(f"/users/{self.user_id}/edit", follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 404)

    def test_delete_user(self):
        """ Test deleting a user """

        with app.test_client() as client:
            resp = client.post(f"/users/{self.user_id}/delete", follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertNotIn(f'<a href="/users/{self.user_id}">', html)



    
