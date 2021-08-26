from typing import Union

from flask import render_template, session

from config.database import db
from models import User


def render_template_(template_name, **kwargs) -> str:
    user = None
    if session.get('user_id', None):
        user = get_user()
    return render_template(template_name, **kwargs, user=user)


def user_has_access_level(user_role: int = 3) -> bool:
    user = get_user()
    return user and user.user_role >= user_role


def get_user(user_id=None) -> Union[User, None]:
    user = None,
    if not user_id:
        user_id = session.get('user_id', None)
    user = db.session.query(User).get(user_id)
    return user
