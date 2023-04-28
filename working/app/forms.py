# Signup and Login forms
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import (
    DataRequired, 
    Length,
    Email, 
    EqualTo, 
    ValidationError
)
from .models import Customer

selectAddress = ['Beijing', 'Shanghai', 'Shenzhen']

# contraint on the address 
class SignupForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[
                                Length(min=6),
                                Email(message='Enter a valid email.'),
                                DataRequired()
                            ])
    password = PasswordField('Password', validators=[Length(min=6, message='Select a longer password.'),DataRequired()])
    confirm = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password', message='Passwords must match.')])
    address = SelectField('Delivery Address', choices = selectAddress, validators=[DataRequired()])
    submit = SubmitField('Sign Up')

    def validate_email(self, email):
        # Check if email already exists
        user = Customer.query.filter_by(customer_email=email.data).first()
        if user:
            raise ValidationError('Email already exists')

class LoginForm(FlaskForm):
    # Login and retrieve user
    email = StringField('Email', validators=[
                                Email(message='Enter a valid email.'),
                                DataRequired()
                            ])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')   