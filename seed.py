from models import User, Post, db
from app import app

db.drop_all()
db.create_all()


User.query.delete()

user1 = User(first_name='Genna',
            last_name='Mergola')

user2 = User(first_name='Terry',
            last_name='Chiem')

db.session.add(user1)
db.session.add(user2)
db.session.commit()
