"""Blogly application."""

from flask import Flask, request, redirect, render_template
from models import db, connect_db, User

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

    #users = User.query.all()

    users = User.query.order_by('last_name', 'first_name')

    return render_template("index.html", users = users)

@app.get("/users/new")
def shows_user_form():
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

    return render_template("user.html", user = user)

@app.get("/users/<int:id>/edit")
def shows_edit_form(id):
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
    #flash messages for redirects
    db.session.commit()

    return redirect("/users")

@app.post("/users/<int:id>/delete")
def delete_user(id):
    """Deletes user, returns to users page"""

    user = User.query.get_or_404(id)

    db.session.delete(user)
    db.session.commit()

    return redirect("/users")