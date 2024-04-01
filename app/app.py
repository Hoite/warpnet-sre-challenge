import os
from flask                  import Flask, flash, render_template, url_for, redirect
from flask_sqlalchemy       import SQLAlchemy
from flask_login            import UserMixin, LoginManager, login_user, login_required, logout_user, current_user
from flask_wtf              import FlaskForm
from wtforms                import StringField, PasswordField, SubmitField
from wtforms.validators     import InputRequired, Length, ValidationError
from flask_bcrypt           import Bcrypt

# Create Flask Application
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))  # Define the "basedir" variable
app.config['SQLALCHEMY_DATABASE_URI']   = 'sqlite:///' + os.path.join(basedir, 'sre-challenge.db')
app.config['SECRET_KEY']                = 'CHANGEME!'

# Database
db = SQLAlchemy(app) # Initialize SQLAlchemy
bcrypt = Bcrypt(app) # Initialize Bcrypt

# Login Manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
@login_manager.user_loader
def load_user(user_id): # Login Manager logic
    return User.query.get(int(user_id))

# Create User Model
class User(db.Model, UserMixin):
    id          = db.Column(db.Integer, primary_key=True)
    username    = db.Column(db.String(15), unique=True, nullable=False) # Username must be unique
    password    = db.Column(db.String(80), nullable=False)

# Classes for Forms
## Login Form
class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(
        min=4, max=15)], render_kw={"placeholder": "Username"})
    
    password = PasswordField('password', validators=[InputRequired(), Length(
        min=8, max=80)], render_kw={"placeholder": "Password"})
    
    submit = SubmitField('Login')

## Register Form
class RegisterForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(
        min=4, max=15)], render_kw={"placeholder": "Username"})
    
    password = PasswordField('password', validators=[InputRequired(), Length(
        min=8, max=80)], render_kw={"placeholder": "Password"})
    
    submit = SubmitField('Register')
    # Custom Validation
    def validate_username(self, username):
        existing_user = User.query.filter_by(   
            username=username.data).first()
        if existing_user:
            raise ValidationError(
                'That username is taken. Please choose a different one.')

# Create Database
app.app_context().push()
with app.app_context(): # Create the database
    db.create_all()

# Routes
# Index Route
@app.route("/")
def index():
    return render_template("index.html", is_authenticated=is_authenticated()) # Render index page passing is_authenticated variable to HTML template

# Register Route
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm() # Initialize the register form

    if form.validate_on_submit(): # Check if form is submitted and validated
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')     # Hash the password
        user = User(username=form.username.data, password=hashed_password) # Create a new user
        db.session.add(user) # Add the user to the database
        db.session.commit() # Commit the transaction to db
        return redirect(url_for('index')) # Redirect to index page after successful registration

    return render_template('register.html', form=form) # Render register page with form

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()  # Initialize the login form
    if form.validate_on_submit():  # Check if form is submitted and validated
        user = User.query.filter_by(username=form.username.data).first()  # Query user by username
        if user and bcrypt.check_password_hash(user.password, form.password.data):  # If user is found and password matches
            login_user(user)  # Log in the user
            return redirect(url_for('index'))  # Redirect to index page after successful login
        else:
            flash('Invalid username or password. Please try again.', 'error')  # Flash an error message
            return render_template('login.html', form=form)  # Render login page with form and error message
    return render_template('login.html', form=form)  # Render login page with form

@app.route("/logout")
@login_required
def logout():
    logout_user() # Log out the user
    return redirect(url_for("index"))

# Check if user is authenticated, functionality for HTML templates
def is_authenticated():
    return current_user.is_authenticated

# Run application
if __name__ == '__main__': # dunder name dunder main
    app.run(debug=True)