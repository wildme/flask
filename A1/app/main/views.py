import os
from flask import render_template, redirect, url_for, flash
from flask import current_app, send_from_directory
from . import main
from .. import db
from ..models import Outbox, User
from .forms import OutboxNew, OutboxEdit
from flask_login import current_user
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
def files(f):
    app = current_app._get_current_object()
    return send_from_directory(app.config['UPLOAD_DIR'], f)

@main.route('/outbox/<out_id>')
def delout(out_id):
    del_item = Outbox.query.filter_by(id=out_id).first() 
    db.session.delete(del_item)
    db.session.commit()
    flash('Letter %s has been deleted' % out_id)
    return redirect(url_for('main.index'))

@main.route('/outbox/edit/<out_id>', methods=['GET', 'POST'])
def editout(out_id):
    o = Outbox.query.get(out_id)
    form = OutboxEdit()
    app = current_app._get_current_object()
    f = form.attachment.data

    if f:
        filename = secure_filename(f.filename)
        f.save(os.path.join(app.config['UPLOAD_DIR'], filename))
    if form.validate_on_submit():
        o.subject=form.subject.data
        o.recipient=form.recipient.data
        o.notes=form.notes.data
        o.attachment=filename
        db.session.commit()
        flash('Letter %s has been updated' % out_id)
        return redirect(url_for('main.index'))
    form.subject.data = o.subject
    form.recipient.data = o.recipient
    form.notes.data = o.notes
    return render_template('/outbox/edit.html', form=form)

@main.route('/inbox/new', methods=['GET', 'POST'])
def inbox_new():
    return render_template('/inbox/new.html')
