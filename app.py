from flask import Flask, render_template, redirect, session, flash
from models import db, connect_db, User
from forms import CreateUserForm, LoginForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///flask_feedback'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()

app.config['SECRET_KEY'] = "itsasecret"


@app.route('/')
def index():
    """Redirect the user to the registration page unless they are logged in."""

    return redirect('/register')


@app.route('/register', methods=['GET', 'POST'])
def submit_register_form():
    """Submits the user registration form."""

    form = CreateUserForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        new_user = User.register(username, password, email, 
                                 first_name, last_name)

        db.session.add(new_user)
        db.session.commit()
        session["username"] = new_user.username

        return redirect(f"/users/{new_user.username}")
    else:
        return render_template('register.html', form=form)
    

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Show a form for logging in."""

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)

        if user:
            session["username"] = user.username
            return redirect(f"/users/{user.username}")
        else:
            form.password.errors = ["You entered an incorrect username or password."]
        
    return render_template("login.html", form=form)


@app.route('/secret')
def secret():
    """Shows the secret page you can only see when logged in, shhh!"""

    if "username" not in session:
        flash("You must be logged in to view this page!")
        return redirect("/")
    else:
        return render_template('secret.html')

@app.route('/logout')
def logout():
    """Log out the user."""

    session.pop("username")

    return redirect("/")

@app.route('/users/<username>')
def user_info(username):
    """Display the user information page."""

    authenticated_user = User.query.filter_by(username=username).first()

    if "username" not in session:
        flash("You must be logged in to view this page!")
        return redirect("/")
    else:
        return render_template('user-info.html', 
                               user=authenticated_user)
