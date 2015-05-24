import requests

import json
from models import Vendor, Deal, Product

product_url = 'https://ineed-db.mybluemix.net/api/items'
createDeal_url = 'http://ineed-dealqq.mybluemix.net/createDeal'
deleteDeal_url = 'http://ineed-dealqq.mybluemix.net/deleteDeal'
getDeal_url = 'http://ineed-dealqq.mybluemix.net/getOneDeal'
id_field = '_id'


def deals_to_json(deal, vendorName, vendorId):
    deal_json = {}
    deal_json['dealName'] = deal.name
    deal_json['vendorName'] = vendorId
    deal_json['vendorId'] = vendorName
    deal_json['type'] = deal.category
    deal_json['price'] = deal.price
    deal_json['discount'] = deal.discount
    deal_json['expireDate'] = deal.expiry_date
    deal_json['couponCode'] = deal.description
    deal_json['redeemCount'] = 10
    deal_json['sendCount'] = 10
    deal_json['itemSell'] = ["555080d16f2b4e2b0097580b", "5550fd3d6f2b4e2b0097580d"]
    return deal_json

def get_single_deal(vendorId, dealName):
    params = {"vendorId": vendorId, "dealName": dealName}
    r = requests.get(getDeal_url, params=params)
    deals = r.json()

    if len(deals) == 0 or deals is None:
        print "No deals with vendorId found"

    deal = deals[0]
    deal_id = deal[id_field]
    return deal_id, deal

def post_single_deal(vendorId, deal, vendorName):
    deal_json = deals_to_json(deal, vendorId, vendorName)
    for k,v in deal_json.items():
        print k, type(v),v
    r = requests.post(createDeal_url, data=deal_json)
    print "Posting single deal", r
    return r


def delete_single_deal(vendorId, deal, vendorName):
    params = {"vendorId": vendorId, "dealName": deal.name}
    r = requests.get(getDeal_url, params=params)
    try:
        deals = r.json()
        deal_id = deals[0][id_field]
        r = requests.delete(deleteDeal_url + '/' + deal_id)
        print "Deleting single deal", r
    except:
        print "No such deals found in database"


