"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy


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

    def __repr__(self):
        """ Show user details """
        
        return f"<User {self.id} {self.first_name} {self.last_name} {self.image_url}>"