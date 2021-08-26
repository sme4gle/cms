from datetime import datetime
from typing import Union

from flask import redirect, request, session

from config.database import db
from controllers import app
from models import Comment, Post, User
from utils.utils import get_user, render_template_, user_has_access_level


@app.route('/edit_post')
@app.route('/edit_post/<post_id>')
def edit_post(post_id: int = None) -> Union[str, redirect]:
    post = None
    user = None
    user_id = session.get('user_id', None)
    if post_id:
        post = db.session.query(Post).get(post_id)
    if user_id:
        user = db.session.query(User).get(user_id)

    if not post:
        if user_has_access_level(2):
            return render_template_('edit_post.html')

    elif post_id and post:
        if user_has_access_level(2) and user_is_post_creator(post.id) or user_has_access_level(3):
            return render_template_('edit_post.html', post=post)

    else:
        return redirect('/')


@app.route('/edit_post_submit', methods=['POST'])
def edit_post_submit():
    data = request.form
    post_id = data.get('post_id', None)
    title = data.get('title', None)
    content = data.get('content', None)
    short_content = data.get('short_content', None)
    user = get_user()
    new_post = False
    post = None
    if post_id:
        post = db.session.query(Post).get(post_id)
    if post:
        if user_has_access_level(2) and user_is_post_creator(post.id) or user_has_access_level(3):
            # Check if the currently signed in user has access level 2 and is the creator of this post,
            # Or check that the currently signed in user is admin.
            pass
        else:
            # Returning the user to the homepage. The user doesn't have access to this function.
            return redirect('/')
    elif post_id and not post:
        # Post does not exist
        return redirect('/')

    elif user_has_access_level(2):
        # We are creating a new post. This statement checks if the user is allowed to post posts.
        new_post = True
    else:
        # The currently signed in user has no access to this page.
        return redirect('/')

    now = datetime.now()
    if new_post:
        post = Post(
            created_by=user.id,
            created_date=now,
            edited_date=now,
        )
        db.session.add(post)
    else:
        post.edited_by = user.id
        post.edited_date = now
    post.content = content
    post.short_content = short_content
    post.title = title
    db.session.commit()
    return redirect('/')


@app.route('/delete_post/<post_id>')
def delete_post(post_id):
    post = db.session.query(Post).get(post_id)
    if post:
        if user_is_post_creator(post_id) or user_has_access_level(3):
            db.session.delete(post)
            db.session.commit()
            return redirect('/')
        else:
            return redirect('/')
    else:
        return redirect('/')

@app.route('/submit_comment/<post_id>', methods=['POST'])
def submit_comment(post_id):
    data = request.form
    parent = data.get('parent', None)
    author_id = data.get('user_id', None)
    content = data.get('content')
    comment = Comment(
        post_id=post_id,
        author_id=author_id,
        content=content,
        created_date=datetime.now()
    )
    if parent:
        comment.parent = parent
    db.session.add(comment)
    db.session.commit()
    return redirect(f'/post/{post_id}')



def user_is_post_creator(post_id) -> bool:
    user = get_user()
    post = db.session.query(Post).get(post_id)
    return user.id == post.creator.id
