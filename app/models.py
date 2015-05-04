from werkzeug import generate_password_hash, check_password_hash
from app import db

class Product(db.Document):
    name = db.StringField(max_length=255, required=True)
    description = db.StringField(max_length=255, required=True)

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