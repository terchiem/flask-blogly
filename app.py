"""Blogly application."""

from flask import Flask, render_template, redirect, request
from models import db, connect_db, User
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'aimaoknfoawnraorn'

debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()


@app.route('/')
def show_home_page():
    """ Show home page. """

    return redirect('/users')

@app.route('/users')
def show_all_users():
    """ Show a list of all users. """

    users = User.query.all()

    return render_template('/users.html',
                            users=users)

@app.route('/users/new')
def show_form():
    """ Show form to create user. """

    return render_template('/form.html')

@app.route('/users/new', methods=['POST'])
def create_user():
    """ adding a new user. """

    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    image_URL = request.form.get('image_url') or None

    new_user = User(first_name=first_name, 
                    last_name=last_name, 
                    image_url=image_URL)
    db.session.add(new_user)
    db.session.commit()

    return redirect('/users')

@app.route('/users/<user_id>')
def show_user(user_id):
    """ show the user page """

    user = User.query.get_or_404(user_id)

    return render_template('/user.html',
                            user=user)

@app.route('/users/<int:user_id>/edit')
def show_edit_form(user_id):
    """ show user edit form """
    user = User.query.get_or_404(user_id)

    return render_template('/edit.html',
                            user=user)

@app.route('/users/<int:user_id>/edit', methods=['POST'])
def edit_user(user_id):
    """ edit user. """

    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    image_URL = request.form.get('image_url')

    user = User.query.get_or_404(user_id)
    
    user.first_name=first_name
    user.last_name=last_name
    user.image_url=image_URL

    db.session.commit()


    return redirect('/users')

@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    """ delete user. """

    user = User.query.get_or_404(user_id)

    db.session.delete(user)

    db.session.commit()

    return redirect('/users')
