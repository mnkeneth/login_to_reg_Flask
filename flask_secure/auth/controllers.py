#App Modules.
from flask_secure import app

# System Modules
from flask_security import LoginForm, url_for_security, RegisterForm

# Log in Parameter for Flask_Security
@app.context_processor
def login_context():
    return {
        'url_for_security': url_for_security,
        'login_user_form': LoginForm(),
    }
# Registeration Form for Flask_Security
@app.context_processor
def register_context():
    return {
        'url_for_security': url_for_security,
        'register_user_form': RegisterForm(),
    }
