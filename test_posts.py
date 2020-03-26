from unittest import TestCase
from app import app
from models import User, Post, db

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False
app.config['TESTING'] = True
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()


class PostTestCase(TestCase):
    """ Tests for posts class """

    def setUp(self):
        """ Add sample user """
        
        Post.query.delete()
        User.query.delete()

        user = User(first_name="Test", last_name="User")
        db.session.add(user)
        db.session.commit()
        
        post1 = Post(title="test_post", content="test content for post", user_id=user.id)
        db.session.add(post1)
        db.session.commit()

        self.user_id = user.id
        self.post_id = post1.id

    def tearDown(self):
        """ Clean up any fouled transaction. """

        db.session.rollback()

    def test_post_list(self):
        """ Test post list """

        with app.test_client() as client:
            resp = client.get(f"/users/{self.user_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<ul id="post-list">', html)
            self.assertIn(f'<li><a href="/posts/{ self.post_id }">', html)             
            self.assertIn('test_post', html)
             
          
    def test_post_details(self):
        """ Test post page details """

        with app.test_client() as client:
            resp = client.get(f"/posts/{self.post_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>test_post</h1>', html)
            self.assertIn('<p>test content for post</p>', html)             
            self.assertIn('<p>By Test User</p>', html)

    
    def test_add_post(self):
        """ Test that we can add a post """

        with app.test_client() as client:
            d = {"title": "HEY", "content": "whats up" }
            resp = client.post(f"/users/{self.user_id}/posts/new", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('HEY', html)
            self.assertIn(f'<a href="/posts/{self.post_id + 1}">', html)

    def test_edit_post(self):
        """ Test editing a post """

        with app.test_client() as client:
            d = {"title": "Jane", "post_content": "Smith" }
            resp = client.post(f"/posts/{self.post_id}/edit", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>Jane</h1>', html)
            self.assertIn('<p>Smith</p>', html)             
            self.assertIn('<p>By Test User</p>', html)
    
    def test_empty_edit_post(self):
        """ Test editing a post with empty text boxes """

        with app.test_client() as client:
            resp = client.post(f"/posts/{self.post_id}/edit", follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 404)

    def test_delete_post(self):
        """ Test deleting a post """

        with app.test_client() as client:
            resp = client.post(f"/posts/{self.post_id}/delete", follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertNotIn(f'<a href="/posts/{self.post_id}">', html)