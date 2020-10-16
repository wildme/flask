import os
from flask import render_template, redirect, url_for, flash
from flask import current_app, send_from_directory
from . import main
from .. import db
from ..models import Outbox, User
from .forms import OutboxNew, OutboxEdit, UserEdit, ChangePass
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename
from datetime import datetime

@main.route('/')
def index():
    out_letters = Outbox.query.order_by(Outbox.id.desc()).all()
    q_users = User.query.all()
    d_names = {}
    for u in q_users:
        d_names[u.id] = u.lastname + ' ' + u.firstname
    return render_template('index.html', out_letters=out_letters, d_names=d_names)

@main.route('/outbox/new', methods=['GET', 'POST'])
@login_required
def outbox_new():
    form = OutboxNew()
    app = current_app._get_current_object()
    now = datetime.now()
    dt_str = now.strftime('%Y-%m-%d %H:%M:%S')

    f = form.attachment.data
    if f:
        filename = secure_filename(f.filename)
        f.save(os.path.join(app.config['UPLOAD_DIR'], filename))
    else:
        filename = None
    if form.validate_on_submit():
        outbox = Outbox(subject=form.subject.data,
                user_id = current_user.id,
                recipient=form.recipient.data,
                attachment=filename,
                reg_date=dt_str,
                notes=form.notes.data)
        db.session.add(outbox)
        db.session.commit()
        flash('You have registered a letter')
        return redirect(url_for('main.index'))
    return render_template('/outbox/new.html', form=form)

@main.route('/files/<f>')
@login_required
def files(f):
    app = current_app._get_current_object()
    return send_from_directory(app.config['UPLOAD_DIR'], f)

@main.route('/outbox/<out_id>')
@login_required
def delout(out_id):
    o = Outbox.query.get(out_id) 
    app = current_app._get_current_object()
    os.remove(os.path.join(app.config['UPLOAD_DIR'], o.attachment))
    db.session.delete(o)
    db.session.commit()
    flash('Letter %s has been deleted' % out_id)
    return redirect(url_for('main.index'))

@main.route('/outbox/edit/<out_id>', methods=['GET', 'POST'])
@login_required
def editout(out_id):
    o = Outbox.query.get(out_id)
    form = OutboxEdit()
    app = current_app._get_current_object()
    f = form.attachment.data
    if f:
        filename = secure_filename(f.filename)
        f.save(os.path.join(app.config['UPLOAD_DIR'], filename))
    else:
        filename = None
    if o.attachment and f:
        os.remove(os.path.join(app.config['UPLOAD_DIR'], o.attachment))
    if form.validate_on_submit():
        o.subject=form.subject.data
        o.recipient=form.recipient.data
        o.notes=form.notes.data
        if filename:
            o.attachment=filename
        db.session.commit()
        flash('Letter %s has been updated' % out_id)
        return redirect(url_for('main.index'))
    form.subject.data = o.subject
    form.recipient.data = o.recipient
    form.notes.data = o.notes
    form.attachment.data = o.attachment
    return render_template('/outbox/edit.html', form=form)

@main.route('/user')
@login_required
def user():
    user = User.query.get(current_user.id)
    return render_template('user.html', user=user)

@main.route('/user/edit', methods=['GET', 'POST'])
@login_required
def edit_user():
    user = User.query.get(current_user.id)
    form = UserEdit()
    if form.validate_on_submit():
        current_user.firstname = form.firstname.data
        current_user.lastname = form.lastname.data
        db.session.commit()
        flash('Your profile has been updated')
        return redirect(url_for('.user', user=user))
    form.firstname.data = current_user.firstname
    form.lastname.data = current_user.lastname
    return render_template('user_edit.html', form=form)

@main.route('/user/password', methods=['GET', 'POST'])
@login_required
def change_pass():
    form = ChangePass()
    if form.validate_on_submit():
        if current_user.verify_password(form.passwordOld.data):
            current_user.password = passwordNew = form.passwordNew.data 
            db.session.commit()
            flash('Your password has changed')
            return redirect(url_for('.user', user_id=current_user.id))
        flash('Invalid password')
    return render_template('ch_pass.html', form=form)
@main.route('/inbox/new', methods=['GET', 'POST'])
@login_required
def inbox_new():
    return render_template('/inbox/new.html')
