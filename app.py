import os
from flask import Flask, render_template, redirect, session, flash
from models import User, Note, connect_db, db
from forms import RegisterForm, LoginForm, CSRFProtectForm, AddNoteForm
from constants import SESSION_LOGIN_KEY

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    "DATABASE_URL", 'postgresql:///flask_notes')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "secret"

connect_db(app)


@app.get('/')
def redirect_to_registration():
    """Returns a redirect to /register"""

    return redirect('/register')


@app.route('/register', methods=['GET', 'POST'])
def register():
    # TODO import IntegrityError and try/except
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

        flash("User Registered!")

        return redirect(f'/users/{user.username}')

    else:
        return render_template("register.html", form=form)


@app.route('/login', methods=['GET', 'POST'])
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
            flash("Login Successful.")
            return redirect(f'/users/{user.username}')

        else:
            form.username.errors = ['Invalid username or password']

    return render_template("login.html", form=form)


@app.get('/users/<username>')
def display_user_info(username):
    """ Displays user info and logout button """

    form = CSRFProtectForm()

    if username not in session:
        flash("You don't have access to that page!")
        return redirect('/login')

    user = User.query.get_or_404(username)

    return render_template('user_info.html',
                           user=user,
                           notes=user.notes,
                           form=form)


@app.post('/logout')
def logout():
    """ Logs user out and redirects to homepage """

    form = CSRFProtectForm()

    if form.validate_on_submit():
        session.pop(SESSION_LOGIN_KEY, None)
        flash("User logged out.")

    return redirect("/")


@app.post('/users/<username>/delete')
def delete_user(username):
    """ delete a user, log them out and redirect them to homepage """

    form = CSRFProtectForm()

    # TODO: Check if its s a post to the right user

    if form.validate_on_submit():

        user = User.query.get_or_404(username)
        user_notes = user.notes

        db.session.delete(user)
        for note in user_notes:
            db.session.delete(note)
        db.session.commit()

        session.pop(SESSION_LOGIN_KEY, None)
        flash("User deleted.")

    return redirect("/")


@app.post('/notes/<note_id>/delete')
def delete_note(note_id):
    """ deletes a note and redirects back to user details page """

    # TODO: Check if its the right note

    form = CSRFProtectForm()

    if form.validate_on_submit():
        note = Note.query.get_or_404(note_id)

        db.session.delete(note)
        db.session.commit()

        flash("Note deleted.")

    return redirect(f"/users/{note.owner_username}")


@app.route('/users/<username>/notes/add', methods=['GET', 'POST'])
def handle_add_note_form(username):
    """GET: Display add note form
       POST: Process add note form by adding note
             then redirects to /user/<username>"""

    form = AddNoteForm()

    if form.validate_on_submit():

        new_note = Note(
            title=form.title.data,
            content=form.content.data,
            owner_username=username
        )

        db.session.add(new_note)
        db.session.commit()

        flash("Note added.")

        return redirect(f"/users/{username}")

    else:
        return render_template("add_note.html", form=form)


@app.route('/notes/<note_id>/update', methods=['GET', 'POST'])
def handle_update_note_form(note_id):
    """GET: Display edit note form
       POST: Process edit note form by editing not
             then redirects to /user/<username>"""

    note = Note.query.get_or_404(note_id)
    form = AddNoteForm(obj=note)

    if form.validate_on_submit():

        note.title = form.title.data
        note.content = form.content.data

        db.session.commit()

        flash("Note updated.")

        return redirect(f"/users/{note.owner_username}")

    else:
        return render_template("edit_note.html", form=form)
