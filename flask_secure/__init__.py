from flask import Flask, render_template
from dotenv import load_dotenv
from flask_migrate import Migrate

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

# Implementation of flask migrate
migrate = Migrate(app, db)

# Applications import config Modules. 
from flask_secure.auth.models import Role, User
from flask_secure.auth.forms import ExtendedRegisterForm

user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore, register_form=ExtendedRegisterForm)

# Assigning user roles to all the other people who register.
@user_registered.connect_via(app)
def _after_reg_hook(sender, user, **extra):
    user_role = Role.query.filter_by(id=2).first()
    user_datastore.add_role_to_user(user=user, role=user_role)
    db.session.commit()
    return

#++++++++++ Register Blueprint URLs ++++++++++
# Import module files. 
from flask_secure.auth.controllers import create

app.register_blueprint(create)

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