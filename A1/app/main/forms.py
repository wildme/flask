from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, FileField
from wtforms import PasswordField
from flask_wtf.file import FileRequired, FileAllowed
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from ..models import Outbox, User

class UserEdit(FlaskForm):
    firstname = StringField('Firstname',
            validators=[DataRequired(), Length(1, 64),
                Regexp('^[A-Za-z]*$', 0, 'only letters allowed')])
    lastname = StringField('Lastname',
            validators=[DataRequired(), Length(1, 64),
                Regexp('^[A-Za-z]*$', 0, 'only letters allowed')])
    submit =  SubmitField('Save')

class ChangePass(FlaskForm):
    passwordOld = PasswordField('Password',
            validators=[DataRequired()]) 
    passwordNew = PasswordField('New password',
            validators=[DataRequired(), EqualTo('passwordNew2', 
                message='Passwords must match.')])
    passwordNew2 = PasswordField('Confirm password',
            validators=[DataRequired()])
    submit =  SubmitField('Change')

class OutboxNew(FlaskForm):
    subject = StringField('Subject', validators=[DataRequired(), Length(1, 64)])
    recipient = StringField('Recipient', validators=[DataRequired()])
    attachment = FileField('File', validators=[
            FileAllowed(['jpg', 'jpeg', 'png', 'pdf', 'docx', 'doc'],
                'Only jpg, png, PDF, doc(x)')])
    notes = StringField('Notes', validators=[Length(1, 128)])
    submit =  SubmitField('Add')

class OutboxEdit(OutboxNew, FlaskForm):
    submit =  SubmitField('Save')
