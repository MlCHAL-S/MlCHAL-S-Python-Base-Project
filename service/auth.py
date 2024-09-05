from . import app, db
from service.models import User
from flask import request, jsonify, render_template, session, flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash


@app.route('/register', methods=('POST', 'GET'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None
        user = User.query.filter_by(username=username).first()

        if not username:
            error = 'Username is required'
        elif not password:
            error = 'Password is required'
        elif user:
            error = 'User already exists'

        if error is None:
            hashed_password = generate_password_hash(password, method='pbkdf2')
            new_user = User(username=username, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()

            return redirect(url_for('login'))

        flash(error)

    return render_template('auth/register.html')


@app.route('/login', methods=('POST', 'GET'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None
        user = User.query.filter_by(username=username).first()
        print(user)

        if user is None:
            error = 'Incorrect username'
        elif not check_password_hash(user.password, password):
            error = 'Incorrect password'

        if error is None:
            session.clear()
            session['user_id'] = user.id
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))
