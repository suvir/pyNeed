# For Flask
WTF_CSRF_ENABLED = False
SECRET_KEY = 'mysecretkeyissecret'

# URL for GeoCoding from Google Maps API
GOOGLE_GEOCODE_URL = 'http://maps.googleapis.com/maps/api/geocode/json?'

# Miscellaneous settings
ID_FIELD = '_id'

# URLs to access Team 10's database
VENDOR_URL = 'https://ineed-db.mybluemix.net/api/vendors'
PRODUCT_URL = 'https://ineed-db.mybluemix.net/api/items'
DB_TRANSACTIONS_URL = "https://ineed-db.mybluemix.net/api/orders"

# URLs to access Orders and Transactions team API
GET_TRANSACTIONS_URL = "http://orders.mybluemix.net/api/v1/vendors/"

# URLs to access Deals team API
CREATE_DEAL_URL = 'http://ineed-dealqq.mybluemix.net/createDeal'
DELETE_DEAL_URL = 'http://ineed-dealqq.mybluemix.net/deleteDeal'
GET_DEAL_URL = 'http://ineed-dealqq.mybluemix.net/getOneDeal'
FIND_DEAL_URL = 'http://ineed-dealqq.mybluemix.net/findDeal'
