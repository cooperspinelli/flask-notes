import os
from flask import Flask, render_template, redirect, session, flash
from models import User, connect_db, db
from forms import RegisterForm, LoginForm, CSRFProtectForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    "DATABASE_URL", 'postgresql:///flask_notes')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "secret"

connect_db(app)

SESSION_LOGIN_KEY = 'username'


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

        session[SESSION_LOGIN_KEY] = user.username

        return redirect(f'/users/{user.username}')

    else:
        return render_template("register.html", form=form)


@app.route('/login', methods=['Get', 'POST'])
def login():
    """GET: Display login form
       POST: Process login form by adding username to session
             then redirects to /user/<username>"""

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        pwd = form.password.data

        user = User.authenticate(username, pwd)

        if user:
            session[SESSION_LOGIN_KEY] = user.username
            return redirect(f'/users/{user.username}')

        else:
            form.username.errors = ['Invalid username or password']

    else:
        return render_template("login.html", form=form)


@app.get('/users/<username>')
def display_user_info(username):
    """ Displays user info and logout button """

    form = CSRFProtectForm()

    if session.get('username') != username:
        flash("You dont have access to that page!")
        return redirect('/login')

    user = User.query.get_or_404(username)
    notes = user.notes

    return render_template('user_info.html',
                           user=user,
                           notes=notes,
                           form=form)




@app.post('/logout')
def logout():
    """ Logs user out and redirects to homepage """

    form = CSRFProtectForm()

    if form.validate_on_submit():
        session.pop("username", None)

    return redirect("/")



"""
TODO:

post request to delete user
post request to delete note

route for add note form (bth get and post)
this will be a single view function
and add html and note form

route for update note form (both get and post)
this will be a single view function
and add html
"""