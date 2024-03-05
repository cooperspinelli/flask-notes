import os
from flask import Flask, render_template, redirect, session
from models import User, connect_db, db
from forms import RegisterForm

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
def register():
    """GET: Display registration form
       POST: Process registration form by adding new user
             then redirects to /user/<username>"""

    form = RegisterForm()

    if form.validate_on_submit():
        username = form.username.data
        pwd = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        user = User.register(username, pwd, email, first_name, last_name)
        db.session.add(user)
        db.session.commit()

        session["username"] = user.username

        return redirect(f'/users/{user.username}')

    else:
        return render_template("register.html", form=form)

