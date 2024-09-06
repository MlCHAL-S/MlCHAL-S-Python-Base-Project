# service/auth/views.py

from flask import Blueprint, request, render_template, session, flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from service.models import User
from service.extensions import db

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=('POST', 'GET'))
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
            flash('Registration successful! You can now log in.', 'success')
            return redirect(url_for('auth.login'))

        flash(error, 'danger')

    return render_template('auth/register.html')


@auth_bp.route('/login', methods=('POST', 'GET'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None
        user = User.query.filter_by(username=username).first()

        if user is None:
            error = 'Incorrect username'
        elif not check_password_hash(user.password, password):
            error = 'Incorrect password'

        if error is None:
            session.clear()
            session['user_id'] = user.id
            flash('Login successful!', 'success')
            return redirect(url_for('posts.index'))

        flash(error, 'danger')

    return render_template('auth/login.html')


@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully.', 'success')
    return redirect(url_for('posts.index'))
