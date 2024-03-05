import os
from flask import Flask, render_template, redirect
from models import connect_db, db
# from forms import

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    "DATABASE_URL", 'postgresql:///pulse37')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "secret"

connect_db(app)

# TODO: Ask if there is database validation for emails (sqlalchemy constraint

@app.get('/')
def redirect_to_registration():
    """Returns a redirect to /register"""

    return redirect('/register')

@app.route('/register', methods=['GET', 'POST'])
def display_registration_form():
    """GET: Display registration form
       POST: Process registration form by adding new user
             then redirects to /user/<username>"""


