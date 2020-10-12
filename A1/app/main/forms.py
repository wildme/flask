from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, FileField
from flask_wtf.file import FileRequired, FileAllowed
from wtforms.validators import DataRequired, Length
from ..models import Outbox

class OutboxNew(FlaskForm):
    subject = StringField('Subject', validators=[DataRequired(), Length(1, 64)])
    recipient = StringField('Recipient', validators=[DataRequired()])
    attachment = FileField('File', validators=[
            FileAllowed(['jpg', 'png', 'pdf', 'docx', 'doc'],
                'Only jpg, png, PDF, doc(x)')])
    notes = StringField('Notes', validators=[Length(1, 128)])
    submit =  SubmitField('Add')
