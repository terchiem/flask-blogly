"""Blogly application."""

from flask import Flask, render_template, redirect, request, abort
from models import db, connect_db, User, Post, Tag
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

    first_name = request.form.get('first_name') or abort(404)
    last_name = request.form.get('last_name') or abort(404)
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

################################################################

@app.route('/users/<int:user_id>/posts/new')
def show_post_form(user_id):
    """ Show form to add a post for that user """

    user = User.query.get_or_404(user_id)
    tags = Tag.query.all()

    return render_template('/post_form.html',
                            user=user,
                            tags=tags)

@app.route('/users/<int:user_id>/posts/new', methods=['POST'])
def make_post(user_id):
    """ Create a post from the user """

    title = request.form.get("title")
    content = request.form.get("content")

    tags_checked = request.form.getlist("tags")
    
    user = User.query.get_or_404(user_id)

    new_post = Post(title=title, 
                    content=content,
                    user_id=user_id)

    for tag_string in tags_checked:
        tag = Tag.query.filter_by(name=tag_string).one()
        new_post.tags.append(tag)
    
    db.session.add(new_post)
    db.session.commit()

    return redirect(f"/users/{user_id}")

@app.route('/posts/<int:post_id>')
def show_post(post_id):
    """ Show post """
    
    post = Post.query.get_or_404(post_id)

    return render_template('/post.html',
                            user=post.user,
                            post=post,
                            tags=post.tags)

@app.route('/posts/<int:post_id>/edit')
def show_edit_post_form(post_id):
    """ Show edit post form """

    post = Post.query.get_or_404(post_id)
    tags = Tag.query.all()
    selected = [ tag.name for tag in post.tags ]

    return render_template('/edit_post.html',
                            post=post,
                            tags=tags,
                            selected=selected)


@app.route('/posts/<int:post_id>/edit', methods=['POST'])
def edit_post(post_id):
    """ edit the post """

    title = request.form.get('title') or abort(404)
    content = request.form.get('post_content') or abort(404)
    selected = request.form.getlist('tags')

    post = Post.query.get_or_404(post_id)
    
    post.title=title
    post.content=content

    post.tags.clear()

    for tag_string in selected:
        tag = Tag.query.filter_by(name=tag_string).one()
        post.tags.append(tag)
   
    db.session.commit()

    return redirect(f"/posts/{post_id}")

@app.route('/posts/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id):
    """ delete post. """

    post = Post.query.get_or_404(post_id)

    db.session.delete(post)
    db.session.commit()

    return redirect(f'/users/{post.user_id}')

################################################################

@app.route('/tags')
def show_tag_list():
    """ Show a list of all tags """

    tags = Tag.query.all()

    return render_template('/tags.html',
                            tags=tags)

@app.route('/tags/<int:tag_id>')
def show_tag_details(tag_id):
    """ Show detail about a tag """

    tag = Tag.query.get_or_404(tag_id)

    return render_template('/tag.html',
                            tag=tag)


@app.route('/tags/new')
def show_tag_form():
    """ Show form to create new tag """

    return render_template('/tag_form.html')


@app.route('/tags/new', methods=['POST'])
def create_tag():
    """ Create a new tag """

    name = request.form.get('name') or abort(404)

    tag = Tag(name=name)

    db.session.add(tag)
    db.session.commit()

    return redirect('/tags')

@app.route('/tags/<int:tag_id>/edit')
def show_edit_tag_form(tag_id):
    """ Show form to edit a tag """

    tag = Tag.query.get_or_404(tag_id)

    return render_template('/edit_tag.html',
                            tag=tag)

@app.route('/tags/<int:tag_id>/edit', methods=['POST'])
def edit_tag(tag_id):
    """ Edit a tag """

    name = request.form.get('name') or abort(404)
    
    tag = Tag.query.get_or_404(tag_id)
    
    tag.name = name   
    db.session.commit()

    return redirect('/tags')


@app.route('/tags/<int:tag_id>/delete', methods=['POST'])
def delete_tag(tag_id):
    """ Delete a tag """

    tag = Tag.query.get_or_404(tag_id)

    db.session.delete(tag)
    db.session.commit()

    return redirect('/tags')

