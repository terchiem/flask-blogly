"""Blogly application."""

from flask import Flask, render_template, redirect
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

