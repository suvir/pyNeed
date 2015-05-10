from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, SelectField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Required

class RequiredIf(Required):
    # a validator which makes a field required if
    # another field is set and has a truthy value

    def __init__(self, other_field_name, *args, **kwargs):
        self.other_field_name = other_field_name
        super(RequiredIf, self).__init__(*args, **kwargs)

    def __call__(self, form, field):
        other_field = form._fields.get(self.other_field_name)
        if other_field is None:
            raise Exception('no field named "%s" in form' % self.other_field_name)
        if bool(other_field.data):
            super(RequiredIf, self).__call__(form, field)

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


class EditProfileForm(Form):
    name = StringField("name", validators=[DataRequired()])
    description = StringField("description")
    email = StringField("email", validators=[DataRequired(), Email()])
    old = PasswordField('Old Password')
    password = PasswordField('New Password', validators=[RequiredIf('old'), EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Repeat New Password', validators=[RequiredIf('old')])
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
    submit = SubmitField("Submit Changes")

class ProductEditRemoveForm(Form):
    name = StringField("name", validators=[DataRequired()])
    description = StringField("description")

class ProductAddForm(Form):
    name = StringField("name", validators=[DataRequired()])
    description = StringField("description")