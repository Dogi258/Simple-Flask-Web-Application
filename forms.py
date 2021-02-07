from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Email, EqualTo

# A custom class 'LoginForm' is created, inheriting from 'FlaskForm'
# This class will be used to render forms in my HTML templates
class SignUpForm(FlaskForm):
    name = StringField('Full Name', validators = [InputRequired()])
    email = StringField('Email', validators = [InputRequired(), Email()])
    password = PasswordField('Password', validators = [InputRequired()])
    confirmPassword = PasswordField('Confirm Password', validators=[InputRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    email = StringField('Email', validators = [InputRequired(), Email()])
    password = PasswordField('Password', validators = [InputRequired()])
    submit = SubmitField('Login')

class EditPetForm(FlaskForm):
    name = StringField("Pet's Name: ")
    age = StringField("Pet's Age: ")
    bio = StringField("Pet's Bio: ")
    submit = SubmitField('Edit Pet')