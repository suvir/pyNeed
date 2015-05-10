from flask.ext.wtf import Form
from wtforms import StringField, FloatField, PasswordField, SelectField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo

class LoginForm(Form):
    email = StringField("email", validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])

class SignupForm(Form):

    name = StringField("name", validators=[DataRequired()])
    description = StringField("description")
    email = StringField("email", validators=[DataRequired(), Email()])
    password = PasswordField('password',
                             validators=[DataRequired(), EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Repeat Password', validators=[DataRequired()])
    category = SelectField("Type of Business", choices=[('restaurant', "Restaurant"), ('cafe', 'Cafe')])
    phone = StringField("Phone number")
    address = StringField("Address of business")
    city = StringField("City")
    state = SelectField("State",
                        choices=[('AK', 'Alaska'), ('AL', 'Alabama'), ('AR', 'Arkansas'), ('AS', 'American Samoa'),
                                 ('AZ', 'Arizona'), ('CA', 'California'), ('CO', 'Colorado'), ('CT', 'Connecticut'),
                                 ('DC', 'District of Columbia'), ('DE', 'Delaware'), ('FL', 'Florida'),
                                 ('GA', 'Georgia'), ('GU', 'Guam'), ('HI', 'Hawaii'), ('IA', 'Iowa'), ('ID', 'Idaho'),
                                 ('IL', 'Illinois'), ('IN', 'Indiana'), ('KS', 'Kansas'), ('KY', 'Kentucky'),
                                 ('LA', 'Louisiana'), ('MA', 'Massachusetts'), ('MD', 'Maryland'), ('ME', 'Maine'),
                                 ('MI', 'Michigan'), ('MN', 'Minnesota'), ('MO', 'Missouri'),
                                 ('MP', 'Northern Mariana Islands'), ('MS', 'Mississippi'), ('MT', 'Montana'),
                                 ('NA', 'National'), ('NC', 'North Carolina'), ('ND', 'North Dakota'),
                                 ('NE', 'Nebraska'), ('NH', 'New Hampshire'), ('NJ', 'New Jersey'),
                                 ('NM', 'New Mexico'), ('NV', 'Nevada'), ('NY', 'New York'), ('OH', 'Ohio'),
                                 ('OK', 'Oklahoma'), ('OR', 'Oregon'), ('PA', 'Pennsylvania'), ('PR', 'Puerto Rico'),
                                 ('RI', 'Rhode Island'), ('SC', 'South Carolina'), ('SD', 'South Dakota'),
                                 ('TN', 'Tennessee'), ('TX', 'Texas'), ('UT', 'Utah'), ('VA', 'Virginia'),
                                 ('VI', 'Virgin Islands'), ('VT', 'Vermont'), ('WA', 'Washington'), ('WI', 'Wisconsin'),
                                 ('WV', 'West Virginia'), ('WY', 'Wyoming')])
    submit = SubmitField("Register")

class ProductEditRemoveForm(Form):
    name = StringField("name", validators=[DataRequired()])
    description = StringField("description")

class ProductAddForm(Form):
    name = StringField("name", validators=[DataRequired()])
    description = StringField("description")

class DealForm(Form):
    deal_name = StringField("deal_name", validators=[DataRequired()])
    product_name = StringField("prod_name", validators=[DataRequired()])
    description = StringField("description")
    price = FloatField("price", validators = [DataRequired()])

class EditProfileForm(Form):
    name = StringField("name", validators=[DataRequired()])
    description = StringField("description")
    email = StringField("email", validators=[DataRequired(), Email()])
    category = SelectField("Type of Business", choices=[('restaurant', "Restaurant"), ('cafe', 'Cafe')])
    phone = StringField("Phone number")
    address = StringField("Address of business")
    city = StringField("City")
    state = SelectField("State",
                        choices=[('AK', 'Alaska'), ('AL', 'Alabama'), ('AR', 'Arkansas'), ('AS', 'American Samoa'),
                                 ('AZ', 'Arizona'), ('CA', 'California'), ('CO', 'Colorado'), ('CT', 'Connecticut'),
                                 ('DC', 'District of Columbia'), ('DE', 'Delaware'), ('FL', 'Florida'),
                                 ('GA', 'Georgia'), ('GU', 'Guam'), ('HI', 'Hawaii'), ('IA', 'Iowa'), ('ID', 'Idaho'),
                                 ('IL', 'Illinois'), ('IN', 'Indiana'), ('KS', 'Kansas'), ('KY', 'Kentucky'),
                                 ('LA', 'Louisiana'), ('MA', 'Massachusetts'), ('MD', 'Maryland'), ('ME', 'Maine'),
                                 ('MI', 'Michigan'), ('MN', 'Minnesota'), ('MO', 'Missouri'),
                                 ('MP', 'Northern Mariana Islands'), ('MS', 'Mississippi'), ('MT', 'Montana'),
                                 ('NA', 'National'), ('NC', 'North Carolina'), ('ND', 'North Dakota'),
                                 ('NE', 'Nebraska'), ('NH', 'New Hampshire'), ('NJ', 'New Jersey'),
                                 ('NM', 'New Mexico'), ('NV', 'Nevada'), ('NY', 'New York'), ('OH', 'Ohio'),
                                 ('OK', 'Oklahoma'), ('OR', 'Oregon'), ('PA', 'Pennsylvania'), ('PR', 'Puerto Rico'),
                                 ('RI', 'Rhode Island'), ('SC', 'South Carolina'), ('SD', 'South Dakota'),
                                 ('TN', 'Tennessee'), ('TX', 'Texas'), ('UT', 'Utah'), ('VA', 'Virginia'),
                                 ('VI', 'Virgin Islands'), ('VT', 'Vermont'), ('WA', 'Washington'), ('WI', 'Wisconsin'),
                                 ('WV', 'West Virginia'), ('WY', 'Wyoming')])
    submit = SubmitField("Register")