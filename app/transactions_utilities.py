__author__ = 'nemanjaa'
import requests
import db_utilities as dbutil
from models import Transaction, Vendor

#?vendorId=VENDORID
get_transactions_url = "http://orders2.mybluemix.net/getTransactionHistory.php"
db_transactions_url = "https://ineed-db.mybluemix.net/api/orders"

def get_transactions_for_vendor_email(vendor_email):
    vendorId, vendor = dbutil.get_vendor_from_db(vendor_email)
    params = {}
    r = requests.get(get_transactions_url, params=params)

    try:
        transactions = r.json()
    except ValueError:
        transactions = {}
    #print transactions
    transaction_list = []
    if len(transactions) != 0:
        for t in transactions:
            if t['vendorId'] == vendorId:
                transaction_list.append(Transaction(payment_type=t['payment_type'], tax=t['tax'], total=t['total'], deal_id=t['deal_id'], discount=t['discount']))

    return transaction_list
