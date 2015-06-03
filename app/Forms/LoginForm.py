from flask.ext.wtf import Form
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email

class LoginForm(Form):
    email = StringField("email", validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
