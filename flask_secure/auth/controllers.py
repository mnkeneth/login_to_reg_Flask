#App Modules.
from flask_secure import app, db
from flask_secure.auth.forms import ExtendedRegisterForm
from flask_secure.auth.models import User

# System Modules
from flask_security import LoginForm, url_for_security, \
                            roles_accepted, registerable, roles_required
from flask import Blueprint, request, render_template, flash, redirect, url_for


create = Blueprint('create', __name__, url_prefix='/create')

# Log in Parameter for Flask_Security
@app.context_processor
def login_context():
    return {
        'url_for_security': url_for_security,
        'login_user_form': LoginForm(),
    }

# Registeration Form for Flask_Security
# To-Do: Define url to be only accessible by the admin users.
@create.route('/user', methods=['GET', 'POST'])
@roles_required("admin")
def create_user():
    form = ExtendedRegisterForm(request.form)
    if request.method == 'GET':
        return render_template('security/register_user.html', 
                            form=form)
                            
    elif request.method == 'POST' and form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        user_exists = db.session.query(User).filter_by(email=email).first()
        if user_exists == True:
            form.email.errors.append(email + ' is already associated with another user')
            form.email.data = str(email)
            return render_template('security/register_user.html', 
                                    form=form)

        else:
            registerable.register_user(
                username = username,
                email = email,
                password=password
                )
            return redirect(url_for('home'))
    
    return render_template('security/register_user.html', 
                            form=form)