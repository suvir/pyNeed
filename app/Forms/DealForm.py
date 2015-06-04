from flask.ext.wtf import Form
from wtforms import StringField, FloatField, SelectField, DateField
from wtforms.validators import DataRequired


class DealForm(Form):
    deal_name = StringField("name", validators=[DataRequired()])
    #product_name = StringField("prod_name", validators=[DataRequired()])
    #description = StringField("description")
    price = FloatField("price", validators=[DataRequired()])
    discount = FloatField("discount", validators=[DataRequired()])
    expiry_date = DateField("expiry_date", validators=[DataRequired()])
    category = SelectField("deal_type", choices=["Deal", "Promotion"])
    coupon_code = StringField("coupon_code")
    item_list = StringField("item_list", validators=[DataRequired()])
