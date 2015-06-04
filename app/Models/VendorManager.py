from Vendor import Vendor
from ProductManager import ProductManager
from DealManager import DealManager
from VendorDao import VendorDao
from werkzeug import generate_password_hash, check_password_hash
from config import GOOGLE_GEOCODE_URL
from app.constants import VENDOR_TYPES
import urllib

try:
    import simplejson
except ImportError:
    import json as simplejson


class VendorManager(object):
    @staticmethod
    def create_vendor(vendor):
        #print "Called factory1"
        v = Vendor(name=vendor['name'], description=vendor['description'], email=vendor['email'],
                   category=vendor['type'],
                   address=vendor['address'], latitude=vendor['coordinates'][0], longitude=vendor['coordinates'][1],
                   phone=vendor['phoneNumber'], state=vendor['state'], city=vendor['city'], pwdhash=vendor['password'])
        return v

    @staticmethod
    def parse_vendor(vendor, products, deals):
        # print "Inside parse vendor"
        # print vendor
        # print products
        # print deals
        v = VendorManager.create_vendor(vendor)

        for prod in products:
            p = ProductManager.create_product(prod)
            v.product_catalog.append(p)

        for deal in deals:
            if 'itemSell' not in deal:
                raise Exception("Unexpected schema change. Expected field itemSell in deal.")
            product_name = ProductManager.get_product_name(deal['itemSell'])
            d = DealManager.create_deal(deal, product_name)
            v.deal_list.append(d)
        return v

    @staticmethod
    def get_vendor(vendor_id=None, email=None):
        if vendor_id is not None:
            vendor = VendorManager.get_vendor_by_id(vendor_id)
            return vendor
        elif email is not None:
            vid, vendor = VendorManager.get_vendor_by_email(email)
            return vid, vendor
        else:
            raise Exception("Called vendor with null id and null email.")

    @staticmethod
    def get_vendor_by_id(vendor_id):
        vendor = VendorDao.get_vendor_by_id(vendor_id)

        if vendor is None or vendor_id is None:
            return None

        # Get all products with matching vendorId
        products = ProductManager.get_all_products_for_vendor(vendor_id)

        # Get all deals with matching vendorId
        deals = DealManager.get_all_deals_for_vendor(vendor_id)

        ret_vendor = VendorManager.parse_vendor(vendor, products, deals)
        return ret_vendor

    @staticmethod
    def get_vendor_by_email(email):
        vendor_id, vendor = VendorDao.get_vendor_by_email(email)

        if vendor is None or vendor_id is None:
            return None, None

        # Get all products with matching vendorId
        products = ProductManager.get_all_products_for_vendor(vendor_id)

        # Get all deals with matching vendorId
        deals = DealManager.get_all_deals_for_vendor(vendor_id)

        ret_vendor = VendorManager.parse_vendor(vendor, products, deals)
        return vendor_id, ret_vendor

    @staticmethod
    def get_all_vendors():
        vendors = VendorDao.get_all_vendors()
        return vendors

    @staticmethod
    def post_vendor(vendor_model):
        vendor = vendor_model.to_json()

        # Post vendor to database and get the id_field in response
        vid = VendorDao.post_vendor(vendor)

        # Post products to database
        ProductManager.post_products_many(vendor_model.product_catalog, vid)
        print "Finished posting products to database"

        # Post deals to database
        DealManager.post_deals_many(vendor_model.deal_list)
        return 0

    @staticmethod
    def put_vendor(vendor_model):
        vendor_json = vendor_model.to_json()
        vendor_id, ignore = VendorManager.get_vendor(email=vendor_json['email'])
        VendorDao.put_vendor(vendor_id, vendor_json)

    @staticmethod
    def get_password_hash(password):
        return generate_password_hash(password)

    @staticmethod
    def check_password(pwdhash, password):
        return check_password_hash(pwdhash, password)

    @staticmethod
    def get_vendor_coordinate(query, from_sensor=False):
        query = query.encode('utf-8')
        params = {
            'address': query,
            'sensor': "true" if from_sensor else "false"
        }
        url = GOOGLE_GEOCODE_URL + urllib.urlencode(params)
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

    @staticmethod
    def get_vendor_types():
        if VENDOR_TYPES is not None:
            return VENDOR_TYPES
        else:
            raise Exception("Vendor Types global list not found!")
