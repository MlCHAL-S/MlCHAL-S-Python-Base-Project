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
            flash(error)
        else:
            user_id = session.get('user_id')  # Ensure user_id is in session
            if user_id is None:
                flash('You must be logged in to create a post')
            else:
                new_post = Post(title=title, body=body, author_id=user_id)
                db.session.add(new_post)
                db.session.commit()
                return redirect(url_for('index'))

    return render_template('posts/create.html')


@app.route('/update', methods=('GET', 'POST'))
def update():
    post = ...  # TODO: GET POST FROM THE DB
    return render_template('posts/update.html', post=post)
