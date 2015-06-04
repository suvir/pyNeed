__author__ = 'suvir'
import requests
from config import FIND_DEAL_URL, ID_FIELD, CREATE_DEAL_URL, DELETE_DEAL_URL, GET_DEAL_URL


class DealDao(object):
    @staticmethod
    def get_all_deals_for_vendor(vendor_id):
        param = {"vendorId": vendor_id}
        r = requests.get(FIND_DEAL_URL, params=param)
        deals = r.json()
        return deals

    @staticmethod
    def post_deal(deal_json):
        r = requests.post(CREATE_DEAL_URL, data=deal_json)
        print "Posting single deal", r
        return r

    @staticmethod
    def delete_deal(vendor_id, deal, vendor_name):
        params = {"deal_id": deal.id}
        r = requests.get(GET_DEAL_URL, params=params)
        try:
            item = r.json()
            deal_id = item[ID_FIELD]
            if deal.id == deal_id:
                    params = {"deal_id": deal.id}
                    r = requests.delete(DELETE_DEAL_URL, params=params)
                    print "Deleting single deal", r
        except:
            print "No such deals found in database"
