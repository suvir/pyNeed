__author__ = 'suvir'
import requests
from config import VENDOR_URL, ID_FIELD

class VendorDao(object):
    @staticmethod
    def get_vendor_by_id(vendorId):
        params = {'_id': vendorId}
        r = requests.get(VENDOR_URL, params=params)
        print r.json()
        vendors = r.json()
        if len(vendors) == 0 or vendors is None:
            print "No vendor with email found"
            return None, None

        vendor = vendors[0]
        print "GETS VENDOR FROM DB"
        print vendor
        return vendor

    @staticmethod
    def get_vendor_by_email(email):
        params = {"email": email}
        r = requests.get(VENDOR_URL, params=params)
        vendors = r.json()
        if len(vendors) == 0 or vendors is None:
            print "No vendor with email found"
            return None, None

        vendor = vendors[0]
        vid = vendor[ID_FIELD]
        return vid, vendor

    @staticmethod
    def get_all_vendors():
        r = requests.get(VENDOR_URL)
        vendors = r.json()
        return vendors

    @staticmethod
    def post_vendor(vendor):
        r = requests.post(VENDOR_URL, data=vendor)
        print r
        if ID_FIELD not in r.json():
            print "Missing id field in response"
            return
        vid = r.json()[ID_FIELD]
        return vid

    @staticmethod
    def put_vendor(vendor_id, vendor_json):
        r = requests.put(VENDOR_URL + '/' + vendor_id, data=vendor_json)
        print r
        return r