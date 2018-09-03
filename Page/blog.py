from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from Page.auth import login_required
from Page.db import get_db
from Page.__init__ import ALLOWED_EXTENSIONS, UPLOAD_FOLDER
import os.path
from werkzeug.utils import secure_filename

bp = Blueprint('blog', __name__)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@bp.route('/')
@login_required
def index():
    db = get_db()
    posts = db.execute(
        'SELECT p.id, title, body, image, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('blog/index.html', posts=posts)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        if request.files: file = request.files['image']
        #image = request.form['image']
        print('\n'+body+'\n')
        error = None
        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)

        if (request.files) and (error is None) and (file.filename != '') and (allowed_file(file.filename)):
            #os.mknod(UPLOAD_FOLDER+'/'+filename)
            #with open(UPLOAD_FOLDER+'/'+filename,'w'): pass
            filename = secure_filename(file.filename)
            out = 'images/'+filename
            file.save(os.path.join(UPLOAD_FOLDER, filename))
        else:
            out = ''
        if error is None:
            db = get_db()
            db.execute(
                'INSERT INTO post (title, body, author_id, image)'
                ' VALUES (?, ?, ?, ?)',
                (title, body, g.user['id'], out)
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/create.html')


def get_post(id, check_author=True):
    post = get_db().execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if post is None:
        abort(404, "Post id {0} doesn't exist.".format(id))

    if check_author and post['author_id'] != g.user['id']:
        abort(403)

    return post


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE post SET title = ?, body = ?'
                ' WHERE id = ?',
                (title, body, id)
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/update.html', post=post)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM post WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('blog.index'))


@bp.route('/calendar')
@login_required
def calendar():
    db = get_db()
    return render_template('blog/calendar.html')
