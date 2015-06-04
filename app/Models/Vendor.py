__author__ = 'suvir'
from app.constants import VENDOR_TYPES

class Vendor(object):
    def __init__(self, name, description, email, category, address, latitude, longitude, phone, state, city, pwdhash):
        self.name = name
        self.description = description
        self.email = email
        self.category = category
        self.address = address
        self.latitude = latitude
        self.longitude = longitude
        self.phone = phone
        self.state = state
        self.city = city
        self.pwdhash = pwdhash
        self.product_catalog = []
        self.deal_list = []

    def to_json(self, ):
        vendor = {}
        vendor['name'] = self.name
        vendor['description'] = self.description
        vendor['email'] = self.email
        vendor['type'] = self.category
        vendor['address'] = self.address
        vendor['coordinates'] = [self.longitude, self.latitude]
        vendor['phoneNumber'] = self.phone
        vendor['state'] = self.state
        vendor['city'] = self.city
        vendor['password'] = self.pwdhash
        vendor['notiPref'] = 'email'
        return vendor
