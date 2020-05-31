from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, ValidationError
from wtforms.validators import DataRequired, Email, length, EqualTo
from flask_login import current_user
#import database handler  once established


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])

    password = PasswordField('Password', validators=[DataRequired()])

    remember = BooleanField("Remember Me")

    submit = SubmitField("Login")


class RegisterForm(FlaskForm):
    name = StringField('Full Name', validators=[DataRequired(), length(min=3,max=25)])

    email = StringField("Email", validators=[DataRequired(), Email()])

    igAccount = StringField("Instagram Username", validators=[DataRequired()])

    password = PasswordField("Password", validators=[DataRequired(),length(min=8)])

    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("password")])

    submit = SubmitField('Sign Up')
    #data validations to make sure that username and email arent in database

