from flask import Flask, render_template
from dotenv import load_dotenv

# Import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc as error

# Flask_Security implementation module
from flask_security import Security, SQLAlchemyUserDatastore, \
                           login_required, current_user, roles_required, user_registered

#Flask email config
from flask_mail import Mail

# VARIABLE PARAMETERS
load_dotenv('.env')

# Configurations
app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('settings.py')
app.debug = True

# Define the database object which is imported
db = SQLAlchemy(app)

# Defining Flask Email parameter ( Not Implemented in this Application )
mail = Mail(app)

# Applications import config Modules. 
from flask_secure.auth.models import Role, User
from flask_secure.auth.forms import ExtendedRegisterForm

user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore, register_form=ExtendedRegisterForm)

# Build the database:
db.create_all()
db.session.commit()

# Creating the roles for the respective users in the system.
try:
    db.session.flush()
    user_datastore.create_role(name='admin', description="Admin Right Used")
    user_datastore.create_role(name="user", description="Normal User Roles")
    db.session.commit()
except error.IntegrityError:
    db.session.rollback()

# Silently Query the first user and giving them admin privileges.
# After registration has already been done.
# Requires re-running the application twice for changes to take effect. 
try:
    admin_user = User.query.filter_by(id=1).first()
    user_role = Role.query.filter_by(id=1).first()
    user_datastore.add_role_to_user(user=admin_user, role=user_role)
    db.session.commit()
except AttributeError: 
    pass

# Assigning user roles to all the other people who register.
@user_registered.connect_via(app)
def _after_reg_hook(sender, user, **extra):
    user_role = Role.query.filter_by(id=2).first()
    user_datastore.add_role_to_user(user=user, role=user_role)
    db.session.commit()
    return

# =================== ALL CONFIGS ABOVE THE LINE. ============================

# Application Home Page Redirect after Login or Registration. 
@app.route("/")
@login_required
def home():
    user = current_user.email
    passwd = current_user.password
    name = current_user.username
    return render_template("home.html", user=user, passwd=passwd, username=name)

@app.route("/admin/")
@roles_required('admin')
def admin():
    user = current_user.email
    passwd = current_user.password
    name = current_user.username
    return render_template("home.html", user=user, passwd=passwd, username=name)