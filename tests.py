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
<<<<<<< HEAD
            self.assertIn('id="user-list-id"', html)
            self.assertNotIn('Test User', html) 
            self.assertNotIn(f'<a href="/users/{self.user_id}">', html)



    # TODO: also test negatives



# from unittest import TestCase

# from app import app
# from models import db, Pet

# # Use test database and don't clutter tests with SQL
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///sqla_intro_test'
# app.config['SQLALCHEMY_ECHO'] = False

# # Make Flask errors be real errors, rather than HTML pages with error info
# app.config['TESTING'] = True

# # This is a bit of hack, but don't use Flask DebugToolbar
# app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

# db.drop_all()
# db.create_all()


# class PetViewsTestCase(TestCase):
#     """Tests for views for Pets."""

#     def setUp(self):
#         """Add sample pet."""

#         Pet.query.delete()

#         pet = Pet(name="TestPet", species="dog", hunger=10)
#         db.session.add(pet)
#         db.session.commit()

#         self.pet_id = pet.id

#     def tearDown(self):
#         """Clean up any fouled transaction."""

#         db.session.rollback()

#     def test_list_pets(self):
#         with app.test_client() as client:
#             resp = client.get("/")
#             html = resp.get_data(as_text=True)

#             self.assertEqual(resp.status_code, 200)
#             self.assertIn('TestPet', html)

#     def test_show_pet(self):
#         with app.test_client() as client:
#             resp = client.get(f"/{self.pet_id}")
#             html = resp.get_data(as_text=True)
=======
            self.assertNotIn(f'<a href="/users/{self.user_id}">', html)
>>>>>>> 1194295a319ba8324028aaaacfe1d7e08e332544



    
