# service/posts/views.py

from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from service.models import Post
from service.extensions import db

posts_bp = Blueprint('posts', __name__)


@posts_bp.route('/')
def index():
    posts = Post.query.all()
    return render_template('posts/index.html', posts=posts)


@posts_bp.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required'
        elif not body:
            error = 'Body is required'

        if error is not None:
            flash(error, 'danger')
        else:
            user_id = session.get('user_id')
            if user_id is None:
                flash('You must be logged in to create a post', 'danger')
            else:
                new_post = Post(title=title, body=body, author_id=user_id)
                db.session.add(new_post)
                db.session.commit()
                flash('Post created successfully!', 'success')
                return redirect(url_for('posts.index'))

    return render_template('posts/create.html')


@posts_bp.route('/update/<int:post_id>', methods=('GET', 'POST'))
def update(post_id):
    post = Post.query.get_or_404(post_id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required'
        elif not body:
            error = 'Body is required'

        if error is None:
            post.title = title
            post.body = body
            db.session.commit()
            flash('Post updated successfully!', 'success')
            return redirect(url_for('posts.index'))

        flash(error, 'danger')

    return render_template('posts/update.html', post=post)


@posts_bp.route('/delete/<int:post_id>', methods=['POST'])
def delete(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    flash('Post deleted successfully.', 'success')
    return redirect(url_for('posts.index'))
