from . import app, db
from flask import jsonify, render_template, request, flash, redirect, url_for, session
from service.models import Post, User


@app.route('/')
def index():
    posts = Post.query.all()
    return render_template('posts/index.html', posts=posts)


@app.route('/create', methods=('GET', 'POST'))
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
            flash(error, 'danger')  # Error message in red
        else:
            user_id = session.get('user_id')  # Ensure user_id is in session
            if user_id is None:
                flash('You must be logged in to create a post', 'danger')
            else:
                new_post = Post(title=title, body=body, author_id=user_id)
                db.session.add(new_post)
                db.session.commit()
                flash('Post created successfully!', 'success')  # Success message in green
                return redirect(url_for('index'))

    return render_template('posts/create.html')


@app.route('/update/<int:post_id>', methods=('GET', 'POST'))
def update(post_id):
    post = Post.query.filter_by(id=post_id).first()

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
            post.title = title
            post.body = body
            db.session.commit()
            flash('Post updated successfully!', 'success')
            return redirect(url_for('index'))

    return render_template('posts/update.html', post=post)


@app.route('/delete/<int:post_id>', methods=['POST'])
def delete(post_id):
    post = Post.query.get(post_id)
    db.session.delete(post)
    db.session.commit()
    flash('Post deleted successfully.', 'success')
    return redirect(url_for('index'))
