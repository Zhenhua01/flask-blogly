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
    """ user homepage with list of users and show add button."""
    return redirect("/users")

@app.get("/users")
def users():
    """ user homepage with list of users and show add button."""
    users = User.query.all()
    return render_template("index.html", users=users)

# //the page that brings up the create page

@app.post("/create_user")
def create_user():
    """Add user information and redirects to user detail page"""

    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url']

    user = User(first_name= first_name, last_name=last_name, image_url=image_url)