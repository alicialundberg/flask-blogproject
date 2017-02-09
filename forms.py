from flask_wtf import Form
from wtforms import TextField, SubmitField

from wtforms import validators, ValidationError

class ContactForm(Form):
   name = TextField("Name",[validators.Required("Please enter your name.")])
   email = TextField("Email",[validators.Required("Please enter your email address."),
      validators.Email("Please enter your email address.")])
   submit = SubmitField("Send")
