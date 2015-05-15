import requests
# from flask import jsonify
import json
from models import Vendor, Deal, Product

vendor_url = 'https://ineed-db.mybluemix.net/api/vendors'
deal_url = 'https://ineed-db.mybluemix.net/api/deals'
product_url = 'https://ineed-db.mybluemix.net/api/items'
id_field = '_id'


def __parse_vendor(vendor, products, deals):
    v = Vendor(name=vendor['name'], description=vendor['description'], email=vendor['email'], category=vendor['type'],
               address=vendor['address'], latitude=vendor['coordinates'][0], longitude=vendor['coordinates'][1],
               phone=vendor['phoneNumber'], state=vendor['state'], city=vendor['city'], pwdhash=vendor['password'])

    for prod in products:
        p = Product(id=prod['_id'], name=prod['prodName'], description=prod['prodDesc'], price=prod['price'])
        v.product_catalog.append(p)

    for deal in deals:
        d = Deal(name=deal['dealName'], product_name=get_product_from_id(deal['itemSell']),
                 coupon_code=deal['couponCode'], price=deal['price'], discount=deal['discount'], category=deal['type'],
                 expiry_date=deal['expireDate'])
        v.deal_list.append(d)

    return v


def get_vendor_from_db_by_id(vendor_id):
    """
    A function to make GET requests for vendor, product, deals and wrap them into a single vendor object
    :param email: email address of the vendor GET
    :return: A vendor model object
    """
    vendor = get_vendor_by_id(vendor_id)

    if vendor is None or vendor_id is None:
        return None

    # Get all products with matching vendorId
    param = {"vendorId": vendor_id}
    r = requests.get(product_url, params=param)
    products = r.json()

    # Get all deals with matching vendorId
    param = {"vendorId": vendor_id}
    r = requests.get(deal_url, params=param)
    deals = r.json()
    print vendor
    print products
    print deals
    ret_vendor = __parse_vendor(vendor, products, deals)
    return vendor_id, ret_vendor


def get_vendor_from_db(email):
    """
    A function to make GET requests for vendor, product, deals and wrap them into a single vendor object
    :param email: email address of the vendor GET
    :return: A vendor model object
    """
    vendor_id, vendor = get_single_vendor(email)

    if vendor is None or vendor_id is None:
        return None

    # Get all products with matching vendorId
    param = {"vendorId": vendor_id}
    r = requests.get(product_url, params=param)
    products = r.json()

    # Get all deals with matching vendorId
    param = {"vendorId": vendor_id}
    r = requests.get(deal_url, params=param)
    deals = r.json()

    ret_vendor = __parse_vendor(vendor, products, deals)
    return vendor_id, ret_vendor


def post_vendor_to_db(vendor_model):
    """
    A function to POST a vendor object to central database.
    It takes care of splitting the model object into vendor, product and deals json objects.
    :param vendor_model: A model vendor object
    :return: Nothing
    """
    vendor = vendor_to_json(vendor_model)

    # Post vendor to database and get the id_field in response
    print type(vendor)
    r = requests.post(vendor_url, data=vendor)
    print r
    if id_field not in r.json():
        print "Missing id field in response"
        return

    vid = r.json()[id_field]

    # Post products to database
    for prod in vendor_model.product_catalog:
        post_single_product(vid, prod)
    print "Finished posting products to database"

    # Post deals to database
    for deal in vendor_model.deal_list:
        deal_json = deals_to_json(deal, vid, vendor_model.name)
        r = requests.post(deal_url, data=deal_json)
        print r
    print "Finished posting deals to database"

    return 0


def put_vendor_to_db(vendor_model):
    """
    A function to PUT a vendor object to central database.
    It takes care of splitting the model object into vendor, product and deals json objects.
    :param vendor_model: A model vendor object
    :return: Nothing
    """
    vendor = vendor_to_json(vendor_model)

    # Post vendor to database and get the id_field in response
    vid, ignore = get_single_vendor(vendor['email'])

    # PUT vendor to database
    json_vendor = vendor_to_json(vendor_model)
    r = requests.put(vendor_url + '/' + vid, data=json_vendor)

    return 0


def vendor_to_json(v):
    vendor = {}
    vendor['name'] = v.name
    vendor['description'] = v.description
    vendor['email'] = v.email
    vendor['type'] = v.category
    vendor['address'] = v.address
    vendor['coordinates'] = [v.latitude, v.longitude]
    vendor['phoneNumber'] = v.phone
    vendor['state'] = v.state
    vendor['city'] = v.city
    vendor['password'] = v.pwdhash
    vendor['notiPref'] = 'email'
    # json_object = json.dumps(vendor,indent=4, separators=(',', ': '))
    # print json_object
    return vendor


def product_to_json(prod, vendorId):
    prod_json = {}
    prod_json['prodName'] = prod.name
    prod_json['prodDesc'] = prod.description
    prod_json['price'] = prod.price
    prod_json['quantity'] = 1
    prod_json['category'] = "perishable"
    prod_json['vendorId'] = vendorId
    return prod_json


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


def get_vendor_by_id(vendorId):
    params = {'_id': vendorId}
    r = requests.get(vendor_url, params=params)
    print r.json()
    vendors = r.json()
    if len(vendors) == 0 or vendors is None:
        print "No vendor with email found"
        return None, None

    vendor = vendors[0]
    print "GETS VENDOR FROM DB"
    print vendor
    return vendor


def get_single_vendor(email):
    params = {"email": email}
    r = requests.get(vendor_url, params=params)
    vendors = r.json()
    if len(vendors) == 0 or vendors is None:
        print "No vendor with email found"
        return None, None

    vendor = vendors[0]
    vid = vendor[id_field]
    return vid, vendor


def get_single_deal(vendorId, dealName):
    params = {"vendorId": vendorId, "dealName": dealName}
    r = requests.get(deal_url, params=params)
    deals = r.json()

    if len(deals) == 0 or deals is None:
        print "No deals with vendorId found"

    deal = deals[0]
    deal_id = deal[id_field]
    return deal_id, deal


def get_single_product(vendorId, productName):
    print vendorId, productName
    params = {"vendorId": vendorId, "prodName": productName}
    r = requests.get(product_url, params=params)
    print r
    products = r.json()

    if len(products) == 0 or products is None:
        print "No products with name and vendorId found"

    print products
    product = products[0]
    pid = product[id_field]
    return pid, product


def post_single_product(vendorId, prod):
    product = product_to_json(prod, vendorId)
    print "Posting single product:", product
    r = requests.post(product_url, data=product)
    print "Posting single product", r


def post_single_deal(vendorId, deal, vendorName):
    deal_json = deals_to_json(deal, vendorId, vendorName)
    for k,v in deal_json.items():
        print k, type(v),v
    r = requests.post(deal_url, data=deal_json)
    print "Posting single deal", r


def delete_single_product(vendorId, product):
    print vendorId, product.name
    params = {"vendorId": vendorId, "prodName": product.name}
    r = requests.get(product_url, params=params)
    try:
        products = r.json()
        product_id = products[0][id_field]
        r = requests.delete(product_url + '/' + product_id)
        print r
    except:
        print "No such products found in database"


def delete_single_deal(vendorId, deal, vendorName):
    params = {"vendorId": vendorId, "dealName": deal.name}
    r = requests.get(deal_url, params=params)
    try:
        deals = r.json()
        deal_id = deals[0][id_field]
        r = requests.delete(deal_url + '/' + deal_id)
        print "Deleting single deal", r
    except:
        print "No such deals found in database"


def get_product_from_id(prod_ids):
    if len(prod_ids) == 0 or prod_ids is None:
        return ''

    r = requests.get(product_url + '/' + prod_ids[0])
    try:
        prod = r.json()
    except ValueError:
        print "Encountered error. No product found."
        return ''
    return prod['prodName']
