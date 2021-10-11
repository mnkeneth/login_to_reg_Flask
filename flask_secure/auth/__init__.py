from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc as error
from flask_migrate import Migrate

# Flask_Security implementation module
from flask_security import Security, SQLAlchemyUserDatastore, \
                           login_required, current_user, roles_required, user_registered

# Within system Modules/Files. 
from flask_secure import app, db
# Applications import config Modules. 
from flask_secure.auth.models import Role, User
from flask_secure.auth.forms import ExtendedRegisterForm

user_datastore = SQLAlchemyUserDatastore(db, User, Role)

migrate = Migrate(app, db)

# # Creating a default user at application start-up

@app.before_first_request
def create_user():
    """
    # Querying for Existing email.
    """
    present_user = db.session.query(User).all()
    if present_user is None:
        try:
            user_datastore.create_user(
                username="Default User", 
                email='admin@local.com', 
                password='admin@local'
                )
            db.session.commit()
        except error.IntegrityError:
            pass
    return

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