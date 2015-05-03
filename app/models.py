from werkzeug import generate_password_hash, check_password_hash
from app import db

class Product(db.Document):
    #id = db.StringField(primary_key=True)
    name = db.StringField(max_length=255, required=True)
    description = db.StringField(max_length=255, required=True)

    # def __repr__(self):
    #     return '<Post %r>' % (self.name)

class Vendor(db.Document):
    #id = db.StringField(primary_key=True)
    name = db.StringField(max_length=255, required=True)
    description = db.StringField(max_length=255)
    email = db.StringField(max_length=255, required=True)
    category = db.StringField(max_length=255, required=True)
    address = db.StringField(max_length=255, required=True)
    latitude = db.StringField()
    longitude = db.StringField()
    phone = db.StringField()
    state = db.StringField()
    city = db.StringField()
    product_catalog = db.ListField(db.EmbeddedDocumentField('Product'))
    pwdhash = db.StringField(max_length=255, required=True)

    meta = {
        'indexes': ['-id'],
        'ordering': ['-id']
    }

    # def __init__(self, name, description, email, category, address, phone, state, city):
    #     self.name = name
    #     self.description = description
    #     self.email = email
    #     self.category = category
    #     self.address = address
    #     self.phone = phone
    #     self.state = state
    #     self.city = city
    #
    #     # Set latitude and longitude
    #     if self.address is not None:
    #         self.get_lat_long()
    #
    # def do_something(self):
    #     print "Received a valid vendor for enrollment"
    #
    # def get_lat_long(self):
    #     self.latitude = 50.0
    #     self.longitude = 110.0
    #

    # def set_password(password):
    #     pwdhash = generate_password_hash(password)
    #     return pwdhash

    #
    # def check_password(password):
    #     return check_password_hash(self.pwdhash, password)
    #
    # def __repr__(self):
    #     return '<Vendor %s %s>' % (self.name, self.description)