from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, SelectField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo
from app.Models import VendorManager
from app.constants import US_STATE_LIST


class SignupForm(Form):
    name = StringField("name", validators=[DataRequired()])
    description = StringField("description")
    email = StringField("email", validators=[DataRequired(), Email()])
    password = PasswordField('password',
                             validators=[DataRequired(), EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Repeat Password', validators=[DataRequired()])
    category = SelectField("Type of Business", choices=VendorManager.get_vendor_types())
    phone = StringField("Phone number")
    address = StringField("Address of business")
    city = StringField("City")
    state = SelectField("State",
                        choices=US_STATE_LIST)
    submit = SubmitField("Register")
