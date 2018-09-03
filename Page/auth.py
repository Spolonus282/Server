import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from Page.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        previous = request.form['previous']
        password = request.form['password']
        confirm = request.form['confirm']
        db = get_db()
        error = None
        if not username: username = g.user['username']
        past_user = g.user['username']
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (past_user,)
        ).fetchone()
        if (not confirm and password) or (confirm and not password) or (confirm != password):
            error = 'Passwords must match.'
        elif username!=past_user and (db.execute(
            'SELECT id FROM user WHERE username = ?', (username,)
        ).fetchone() is not None):
            error = 'User {} is already registered.'.format(username)
        elif not previous and any([username!=past_user,password]):
            error = 'Password is required'
        elif previous and not check_password_hash(user['password'], previous):
            print(g.user['password'])
            print(generate_password_hash(previous))
            error = 'Incorrect Password'

        if error is None:
            if password:
                db.execute(
                    'UPDATE user SET password = ? WHERE username = ?',
                    (generate_password_hash(password), past_user))
            if username != past_user:
                db.execute(
                    'UPDATE user SET username = ? WHERE username = ?',(username,past_user)
                )
            db.commit()
            return redirect(url_for('blog.index'))

        flash(error)
    return render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view
