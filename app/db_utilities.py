import requests
from models import Vendor, Deal, Product

vendor_url = 'https://ineed-db.mybluemix.net/api/vendors'
deal_url = 'https://ineed-db.mybluemix.net/api/deals'
product_url = 'https://ineed-db.mybluemix.net/api/items'
id_field = '_id'

def parse_vendor(vendor, products, deals):
	#city = vendor['city']
	city = 'San Diego'
	#state = vendor['state']
	state = 'CA'
	#description = vendor['description']
	description ='dummy description'
	pw = vendor['pwdhash']
	v = Vendor(name=vendor['name'],description=description, email = vendor['email'],\
		category=vendor['type'],address=vendor['address'],latitude=vendor['coordinates'][0],\
		longitude=vendor['coordinates'][1],phone=vendor['phoneNumber'], state=state,city=city,\
		pwdhash=pw)

	for prod in products:
		p = Product(name=prod['productName'],description=prod['description'], price=prod['price'])
		v.product_catalog.append(p)

	for deal in deals:
		d = Deal(name=deal['dealName'],product_name=deal['productName'],description=prod['description'],\
			price=deal['price'],discount=deal['discount'],category=deal['type'],expiry_date=deal['expireDate'])
		v.deal_list.append(d)

	return v

def get_vendor(email):
	vid,vendor = get_single_vendor(email)

	#Get all products with matching vendorId
	param = {"vendorId":vid}
	r = requests.get(product_url, params = param)
	products = r.json()

	#Get all deals with matching vendorId
	param = {"vendorId":vid}
	r = requests.get(deal_url, params = param)
	deals = r.json()

	ret_vendor = parse_vendor(vendor,products,deals)
	return ret_vendor

def post_vendor(v):
	vendor = vendor_to_json(v)

	#Post vendor to database and get the id_field in response
	r=requests.post(vendor_url,data=vendor)
	if id_field not in r.json():
		print "Missind id field in response"
		return

	vid = r.json()[id_field]

	products = [product_to_json(prod,vid) for prod in v.product_catalog]
	deals = [deals_to_json(deal,vid,v.name) for deal in v.deal_list]

	#Post products to database
	r=requests.post(product_url,data=products)
	print "Finished posting products to database"

	#Post deals to database
	r=requests.post(deal_url,data=deals)
	print "Finished posting deals to database"

	return 0

def put_vendor(v):
	vendor = vendor_to_json(v)

	#Post vendor to database and get the id_field in response
	vid,ignore = get_single_vendor(vendor['email'])
	
	#PUT vendor to database
	json_vendor = vendor_to_json(v)
	r=requests.put(vendor_url+'/'+vid,data=json_vendor)

	#PUT products in database	
	for prod in v.product_catalog:
		pid,product = get_single_product(vid,prod.name)
		json_product = product_to_json(product)
		r = requests.put(product_url+'/'+pid, data=json_product)

	#PUT deals in database
	for d in v.deal_list:
		deal_id,deal = get_single_deal(vid,d.name)
		json_deal = deals_to_json(deal)
		r = requests.put(deal_url+'/'+deal_id,data=json_deal)
		
	return 0

def vendor_to_json(v):
	vendor={}
	vendor['name']=v.name
	vendor['description']=v.description
	vendor['email']=v.email
	vendor['type']=v.category
	vendor['address']=v.address
	vendor['coordinates']=[v.latitude,v.longitude]
	vendor['phoneNumber']=v.phone
	vendor['state']=v.state
	vendor['city']=v.city
	vendor['pwdhash']=v.pwdhash
	return vendor

def product_to_json(prod,vendorId):
	p = {}
	p['name']=prod.name
	p['description']=prod.description
	p['price']=prod.price
	p['vendorId']=vendorId
	return product

def deals_to_json(deal,vendorName,vendorId):
	d = {}
	d['dealName']=deal.name
	d['vendorName']=vendorName
	d['vendorId']=vendorId
	d['type']=deal.category
	d['price']=deal.price
	d['discount']=deal.discount
	d['expireDate']=deal.expiry_date
	return d

def get_single_vendor(email):
	param = {"email":email}
	r = requests.get(vendor_url,params=param)
	vendors = r.json()
	
	if len(vendors) == 0 or vendors is None:
		print "No vendor with email found"
		return

	vendor = vendors[0]
	vid = vendor[id_field]
	return vid,vendor

def get_single_product(vendorId,productName):
	params = {"vendorId":vendorId,"productName":productName}
	r = requests.get(product_url,params=params)
	products = r.json()

	if len(products) == 0 or products is None:
		print "No products with name and vendorId found"

	product = products[0]
	pid = product[id_field]
	return pid,product

def get_single_deal(vendorId,dealName):
	params = {"vendorId":vendorId,"dealName":dealName}
	r = requests.get(deal_url,params=params)
	deals = r.json()

	if len(deals) == 0 or deals is None:
		print "No deals with vendorId found"

	deal = deals[0]
	deal_id = deal[id_field]
	return deal_id,deal
