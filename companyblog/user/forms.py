from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo, Email
from wtforms import ValidationError
from flask_wtf.file import FileField, FileAllowed

from flask_login import current_user
from companyblog.model import User

class Loginform(FlaskForm):
    email = StringField('Email:', validators = [DataRequired(), Email()])
    password = PasswordField('Password:', validators = [DataRequired()])
    submit = SubmitField('Login In')

class Register(FlaskForm):
    username = StringField('UserName:', validators = [DataRequired()])
    email = StringField('Email:', validators = [DataRequired(), Email()])
    password = PasswordField('Password:', validators = [DataRequired(), EqualTo('pass_con')])
    pass_con = PasswordField('Confirm Password:', validators = [DataRequired()])
    submit = SubmitField('Register')

    def check_email(self, field):
        if User.query.filter_by(email = field.data).first():
            raise ValidationError('Your email is Already Registered')

    def check_username(self, field):
        if User.query.filter_by(username = field.data).first():
            raise ValidationError('Your username is Already Registered')


class UpdateUserForm(FlaskForm):
    username = StringField('UserName:', validators = [DataRequired()])
    email = StringField('Email:', validators = [DataRequired(), Email()])
    picture = FileField('Update Profile Photo:', validators = [FileAllowed(['jpg','png'])])
    submit = SubmitField('Update')

    def check_email(self, field):
        if User.query.filter_by(email = field.data).first():
            raise ValidationError('Your email is Already Registered')

    def check_username(self, field):
        if User.query.filter_by(username = field.data).first():
            raise ValidationError('Your username is Already Registered')
