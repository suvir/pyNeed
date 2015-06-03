from flask.ext.wtf import Form
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired, Email
from app.Models import VendorManager
from app.constants import US_STATE_LIST

class EditProfileForm(Form):
    name = StringField("name", validators=[DataRequired()])
    description = StringField("description")
    email = StringField("email", validators=[DataRequired(), Email()])
    category = SelectField("Type of Business", choices=VendorManager.get_vendor_types())
    phone = StringField("Phone number")
    address = StringField("Address of business")
    city = StringField("City")
    state = SelectField("State",
                        choices=US_STATE_LIST)
    submit = SubmitField("Register")

if __name__ == "__main__":
    print "Hello form!"
