__author__ = 'suvir'
from werkzeug import generate_password_hash, check_password_hash
from models import Product
import urllib
try:
    import simplejson
except ImportError:
    import json as simplejson

googleGeocodeUrl = 'http://maps.googleapis.com/maps/api/geocode/json?'

def get_password_hash(password):
    return generate_password_hash(password)


def check_password(pwdhash, password):
    return check_password_hash(pwdhash, password)


def parse_product_catalog_multidict(f):
    products = []
    if 'add_qty' in f and 'add_name' in f:
        if len(f['add_qty']) > 0 and len(f['add_name'])>0:
            products.append(Product(name=f['add_qty'], description=f['add_name']))

    product_counter = 1
    next_item_name = 'qty' + str(product_counter)
    next_item_desc = 'name' + str(product_counter)
    while next_item_name in f and next_item_desc in f:
        if len(f[next_item_name]) > 0 and len(f[next_item_desc]) > 0:
            products.append(Product(name=f[next_item_name], description=f[next_item_desc]))
        product_counter += 1
        next_item_name = 'qty' + str(product_counter)
        next_item_desc = 'name' + str(product_counter)
    return products

def parse_product(f):
    product = Product()
    product.name = f['name']
    product.description = f['description']
    return product

def print_product_catalog_multidict(f):
    print "Printing out all received values"
    for key in f:
        for value in f.getlist(key):
            print key, ":", value, type(value)

def get_coordinates(query, from_sensor=False):
    query = query.encode('utf-8')
    params = {
        'address': query,
        'sensor': "true" if from_sensor else "false"
    }
    url = googleGeocodeUrl + urllib.urlencode(params)
    json_response = urllib.urlopen(url)
    response = simplejson.loads(json_response.read())
    if response['results']:
        location = response['results'][0]['geometry']['location']
        latitude, longitude = location['lat'], location['lng']
        print query, latitude, longitude
    else:
        latitude, longitude = None, None
        print query, "<no results>"
    return latitude, longitude