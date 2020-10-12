import os
from flask import render_template, redirect, url_for, flash
from flask import current_app, send_from_directory
from . import main
from .. import db
from ..models import Outbox
from .forms import OutboxNew
from flask_login import current_user
from werkzeug.utils import secure_filename

@main.route('/')
def index():
    out_letters = Outbox.query.order_by(Outbox.id.desc()).all()
    
    return render_template('index.html', out_letters=out_letters)

@main.route('/outbox/new', methods=['GET', 'POST'])
def outbox_new():
    form = OutboxNew()
    app = current_app._get_current_object()
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
                notes=form.notes.data)
        db.session.add(outbox)
        db.session.commit()
        flash('You have registered a letter')
        return redirect(url_for('main.index'))
    return render_template('/outbox/new.html', form=form)

@main.route('/inbox/new', methods=['GET', 'POST'])
def inbox_new():
    return render_template('/inbox/new.html')

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
