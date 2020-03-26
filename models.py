"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy
import datetime


db = SQLAlchemy()

def connect_db(app):
    """ Connect to database. """

    db.app = app
    db.init_app(app)



class User(db.Model):
    """ User Class """

    __tablename__ = "users"

    id = db.Column(db.Integer,
                    primary_key=True,
                    autoincrement=True)
    
    first_name = db.Column(db.String(30),
                            nullable=False)

    last_name = db.Column(db.String(30),
                            nullable=False)

    image_url = db.Column(db.String(50),
                            nullable=True,
                            default="/static/default.png")
    
    posts = db.relationship('Post',
                            backref='user')

    def __repr__(self):
        """ Show user details """
        
        return f"<User {self.id} {self.first_name} {self.last_name} {self.image_url}>"

class Post(db.Model):
    """ Post Class """

    __tablename__ = "posts"

    id = db.Column(db.Integer,
                    primary_key=True,
                    autoincrement=True)

    title = db.Column(db.Text,
                      nullable=False)

    content = db.Column(db.Text,
                        nullable=False)
    
    created_at = db.Column(db.DateTime,
                            default=datetime.datetime.utcnow)
    
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.id'))
    
    def __repr__(self):
        """ Show post details """
        
        return f"<User {self.id} {self.first_name} {self.last_name} {self.image_url}>"