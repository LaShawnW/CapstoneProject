from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, SelectField, SubmitField, BooleanField
from wtforms.validators import DataRequired, InputRequired, Required
from wtforms.validators import Email
from wtforms.fields.html5 import DateField
from wtforms import TimeField


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

class ReservationForm(FlaskForm):
    starttime = TimeField('Arrival Time', validators= [Required()])
    startdate = DateField('Arrival Date', format='%Y-%m-%d')
    endtime = TimeField('Departure Time', validators= [Required()])
    enddate = DateField('Departure Date', format='%Y-%m-%d')
    parkinglots = SelectField('Available Parking', choices=[('Mall Plaza Parking Lot' ,'Mall Plaza Parking Lot'), ('UDC Parking Lot','UDC Parking Lot',), ('New Kingston Parking Lot','New Kingston Parking Lot ',),('SciTech Parking Lot','SciTech Parking Lot')])
    licenseplateno= StringField('License Plate No', validators=[DataRequired()])
    typeofparking = SelectField('Type of Parking', choices=[('Tier 1','Tier 1'), ('Tier 2','Tier 2'), ('Tier 3','Tier 3')])
    
    submit = SubmitField('Reserve')