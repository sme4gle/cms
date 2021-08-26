from typing import Union


from app import db
from controllers import app
from models import Post, Comment
from utils.utils import render_template_


@app.route('/')
def root() -> str:
    most_recent_posts = db.session.query(Post).order_by(db.desc(Post.id)).limit(5)
    return render_template_('index.html', posts=most_recent_posts)


@app.route('/post/<post_id>')
def post(post_id) -> Union[tuple, str]:
    post = db.session.query(Post).get(post_id)
    if post:
        return render_template_('post.html', post=post)
    else:
        return render_template_('errors/404.html'), 404
