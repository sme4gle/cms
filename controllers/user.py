import hashlib
import json

from flask import redirect, request, session
from sqlalchemy import or_

from config.database import db
from controllers import app
from models import User
from utils.utils import render_template_


@app.route('/login')
def login() -> str:
    return render_template_('login.html')


@app.route('/register')
def register() -> str:
    return render_template_('register.html')


@app.route('/do_login', methods=['POST'])
def do_login() -> tuple:
    data = json.loads(request.data.decode())
    username = data.get('username', None)
    password = data.get('password', None)
    response, status = {'response': 'Username or password incorrect'}, 401
    if not username:
        response, status = {'response': 'Missing username'}, 401
    elif not password:
        response, status = {'response': 'Missing password'}, 401
    user = db.session.query(User).filter(or_(User.username == username, User.email == username)).first()
    if user:
        hashed_password = hashlib.sha224(password.encode()).hexdigest()
        if hashed_password == user.password:
            session['user_id'] = user.id
            response, status = {'response': 'Login successful'}, 200
    return response, status


@app.route('/do_register', methods=['POST'])
def do_register() -> tuple:
    data = json.loads(request.data.decode())
    username = data.get('username', None)
    password = data.get('password', None)
    email = data.get('email', None)

    response, status = {}, 500
    if not username or not password or not email:
        response = {'status': 'Required fields are missing.'}
    else:
        try:
            # I'm using a try block here. There's a chance that the username or email are in use, without this try block this would return an error the end user doesn't know what to do with.
            # For this demonstration I'm using sha224 for simplicity, but in a real world example I would have hashed the password using a salt.
            # We do this to make the hash more random. If a user registers an account with a password like `test123` there's a big chance
            # that the hash we store in our database is compromised because of the input being recorded in a bunch of rainbowtables.
            password = hashlib.sha224(password.encode()).hexdigest()
            user = User(
                username=username,
                password=password,
                email=email,
            )
            db.session.add(user)
            response, status = {'response': 'Registration succesful'}, 200
        except:
            response = {'response': 'A user with that username or email exists.'}
        db.session.commit()
    return response, status


@app.route('/logout')
def logout() -> redirect:
    session['user_id'] = None
    return redirect('/')
