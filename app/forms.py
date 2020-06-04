from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField,SelectField,TextAreaField, SubmitField
from wtforms.validators import InputRequired,DataRequired, Email



class UserRegistration(FlaskForm):
 firstname = StringField('First Name', validators=[DataRequired()])
 lastname = StringField('Last Name', validators=[DataRequired()])
 gender = SelectField('Gender', choices=[('Male', 'Male'), ('Female', 'Female')])
 email = StringField('Email', validators=[DataRequired(), Email()])
 password= PasswordField("Password", validators=[InputRequired()])

 submit = SubmitField("Add Account")

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')

class PostForm(Form):
    content = TextAreaField("Type your destination here", validators=[DataRequired(),])