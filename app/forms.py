from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo

class RegistrationForm(FlaskForm):
    email = StringField(validators=[DataRequired(), Email()])
    password = PasswordField(validators=[DataRequired()])
    confirm_password = PasswordField(validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    email = StringField(validators=[DataRequired(), Email()])
    password = PasswordField(validators=[DataRequired()])
    remember_me = BooleanField(label="Remember Me")
    submit = SubmitField('Login')

class ChangeEmailForm(FlaskForm):
    email = StringField(validators=[DataRequired(), Email()])
    confirm_email = StringField(validators=[DataRequired(), Email(), EqualTo('email')])
    submit = SubmitField('Change Email')

class AddressInputForm(FlaskForm):
    address = StringField(validators=[DataRequired()])
    city = StringField()
    state = StringField()
    zipcode = StringField()
    submit = SubmitField('Submit Address')