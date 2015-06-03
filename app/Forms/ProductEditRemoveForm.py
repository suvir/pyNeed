from flask.ext.wtf import Form
from wtforms import StringField
from wtforms.validators import DataRequired


class ProductEditRemoveForm(Form):
    name = StringField("name", validators=[DataRequired()])
    description = StringField("description")
