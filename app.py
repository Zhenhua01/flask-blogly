"""Blogly application."""

from flask import Flask, request, redirect, render_template
from models import db, connect_db, User, Post, Tag, PostTag

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

from flask_debugtoolbar import DebugToolbarExtension
app.config['SECRET_KEY'] = "SECRET!"
debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()


@app.get("/")
def homepage():
    """ redirects to user homepage. """
    return redirect("/users")

@app.get("/users")
def list_users():
    """ shows user homepage with list of users and show add button."""

    # query users list and orders them before returning
    users = User.query.order_by('last_name', 'first_name')

    return render_template("index.html", users = users)

@app.get("/users/new")
def show_new_user_form():
    """ shows add new user form."""

    return render_template("new_user.html")

@app.post("/users/new")
def create_user():
    """Add user information and redirects to user detail page"""

    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url']
    image_url = image_url if image_url else None

    user = User(first_name= first_name, last_name=last_name, image_url=image_url)

    db.session.add(user)
    db.session.commit()

    return redirect("/users")

@app.get("/users/<int:id>")
def get_user(id):
    """Gets user information and shows to page"""

    user = User.query.get_or_404(id)
    posts = user.posts

    return render_template("user.html", user = user, posts = posts)

@app.get("/users/<int:id>/edit")
def show_user_edit_form(id):
    """Shows user edit form"""

    user = User.query.get_or_404(id)

    return render_template("edit_user.html", user = user)

@app.post("/users/<int:id>/edit")
def edit_user(id):
    """Edits user information, updates database, and returns to users page """

    user = User.query.get_or_404(id)

    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']

    db.session.commit()

    return redirect("/users")

@app.post("/users/<int:id>/delete")
def delete_user(id):
    """Deletes user, returns to users page"""

    user = User.query.get_or_404(id)
    posts = user.posts

    db.session.delete(*posts)
    db.session.commit()

    db.session.delete(user)
    db.session.commit()

    return redirect("/users")

# try using post_id and user_id in url route
@app.get("/users/<int:id>/posts/new")
def show_post_form(id):
    """ shows add new post form for user."""

    user = User.query.get_or_404(id)

    return render_template("new_post.html", user = user)

@app.post("/users/<int:id>/posts/new")
def add_post(id):
    """Add post to user, redirects to user page"""

    title = request.form['title']
    content = request.form['content']

    post = Post(title=title, content=content, user_id=id)
    db.session.add(post)
    db.session.commit()

    # add redirect flash message for confirmation
    return redirect(f"/users/{id}")

@app.get("/posts/<int:id>")
def show_post(id):
    """Gets post content and shows to page """

    post = Post.query.get_or_404(id)

    time = post.created_at.strftime('%a, %b %d, %Y %I:%M %p')
    # time = f'{post.created_at:%b %d, %Y}'

    return render_template("post.html", post = post, time = time)

@app.get("/posts/<int:id>/edit")
def show_post_edit_form(id):
    """ Shows post edit form """

    post = Post.query.get_or_404(id)

    return render_template("edit_post.html", post = post)

@app.post("/posts/<int:id>/edit")
def edit_post(id):

    post = Post.query.get_or_404(id)

    post.title = request.form['title']
    post.content = request.form['content']

    db.session.commit()

    return redirect(f"/posts/{id}")

@app.post("/posts/<int:id>/delete")
def delete_post(id):

    post = Post.query.get_or_404(id)

    db.session.delete(post)
    db.session.commit()

    # add redirect flash message for confirmation
    return redirect(f"/users/{post.user_id}")

