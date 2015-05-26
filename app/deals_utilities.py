import requests
import json
from models import Vendor, Deal, Product
#from db_utilities import *
import db_utilities as dbutil

product_url = 'https://ineed-db.mybluemix.net/api/items'
createDeal_url = 'http://ineed-dealqq.mybluemix.net/createDeal'
deleteDeal_url = 'http://ineed-dealqq.mybluemix.net/deleteDeal'
getDeal_url = 'http://ineed-dealqq.mybluemix.net/getOneDeal'
id_field = '_id'


def deals_to_json(deal, vendorName, vendorId):
    deal_json = {}
    deal_json['dealName'] = deal.name
    deal_json['vendorName'] = vendorName
    deal_json['vendorId'] = vendorId
    deal_json['type'] = deal.category
    deal_json['price'] = deal.price
    deal_json['discount'] = deal.discount
    deal_json['expireDate'] = deal.expiry_date
    deal_json['couponCode'] = deal.description
#    deal_json['redeemCount'] = 10
#    deal_json['sendCount'] = 10

    products = []
    prod_id, product = dbutil.get_single_product(vendorId, deal.product_name)
    products.append(str(prod_id))
    deal_json['itemSell'] = products

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
    deal_json = deals_to_json(deal, vendorName, vendorId)
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


