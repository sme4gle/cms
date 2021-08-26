from flask import Blueprint

app = Blueprint('app', __name__)
from .main import root
from .user import do_login
from .posts import edit_post, edit_post_submit, delete_post

from .manage_users import user_list, manage_user, manage_user_submit