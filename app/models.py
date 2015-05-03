from flask.ext.sqlalchemy import SQLAlchemy
from werkzeug import generate_password_hash, check_password_hash

db = SQLAlchemy()


class Vendor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    description = db.Column(db.String(250), index=False, unique=False)
    email = db.Column(db.String(120), index=True, unique=True)
    category = db.Column(db.String(64), index=False, unique=False)
    address = db.Column(db.String(250), index=False, unique=False)
    latitude = db.Column(db.Float, primary_key=False)
    longitude = db.Column(db.Float, primary_key=False)
    phone = db.Column(db.String(64), index=False, unique=False)
    state = db.Column(db.String(64), index=False, unique=False)
    city = db.Column(db.String(64), index=False, unique=False)
    product_catalog = db.relationship('Product', backref='vendor', lazy='dynamic')
    pwdhash = db.Column(db.String(54))

    def __init__(self, name, description, email, category, address, phone, state, city):
        self.name = name
        self.description = description
        self.email = email
        self.category = category
        self.address = address
        self.phone = phone
        self.state = state
        self.city = city

        # Set latitude and longitude
        if self.address is not None:
            self.get_lat_long()

    def do_something(self):
        print "Received a valid vendor for enrollment"

    def get_lat_long(self):
        self.latitude = 50.0
        self.longitude = 110.0

    def set_password(self, password):
        self.pwdhash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.pwdhash, password)

    def __repr__(self):
        return '<Vendor %s %s>' % (self.name, self.description)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(140))
    description = db.Column(db.String(140))
    vendor_id = db.Column(db.Integer, db.ForeignKey('vendor.id'))

    def __repr__(self):
        return '<Post %r>' % (self.name)