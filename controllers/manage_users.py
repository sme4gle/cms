import hashlib

from flask import request
from werkzeug.utils import redirect

from config.database import db
from controllers import app
from models import User
from utils.utils import render_template_, user_has_access_level

user_access = {
    1: 'Gast',
    2: 'Auteur',
    3: 'Admin'
}

@app.route('/users')
def user_list():
    if user_has_access_level(3):
        users = db.session.query(User).all()
        return render_template_('manage_users.html', users=users, user_access=user_access)
    else:
        return redirect('/')


@app.route('/manage_user/<user_id>')
def manage_user(user_id):
    if user_has_access_level(3):
        _user = db.session.query(User).get(user_id)
        if _user:
            return render_template_('manage_user.html', _user=_user, user_roles=user_access)
        else:
            return redirect('/users')
    else:
        # Access is not allowed for this user.
        return redirect('/')


@app.route('/manage_user_submit/<user_id>', methods=['POST'])
def manage_user_submit(user_id):
    if user_has_access_level(3):
        data = request.form
        username = data.get('username', None)
        email = data.get('email', None)
        user_role = data.get('user_role')
        password = data.get('password', None)
        _user = db.session.query(User).get(user_id)
        if _user:
            if username:
                _user.username = username
            if email:
                _user.email = email

            _user.user_role = user_role

            if password:
                hashed_password = hashlib.sha224(password.encode()).hexdigest()
                _user.password = hashed_password
            db.session.commit()
            # User has been modified successfully.
            return redirect('/users')
        else:
            # A user with this user_id has not been found.
            return redirect('/users')
    return redirect('/')
