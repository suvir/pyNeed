from flask.ext.wtf import Form
from wtforms import StringField, FloatField
from wtforms.validators import DataRequired

class ProductAddForm(Form):
    name = StringField("name", validators=[DataRequired()])
    description = StringField("description")
    price = FloatField("price", validators = [DataRequired()])

