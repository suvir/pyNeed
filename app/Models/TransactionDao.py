__author__ = 'suvir'
import requests
from Transaction import Transaction
from config import GET_TRANSACTIONS_URL


class TransactionDao(object):
    @staticmethod
    def get_all_transactions_for_vendor(vendor_id):
        params = {}
        r = requests.get(GET_TRANSACTIONS_URL+str(vendor_id)+"/transactions", params=params)
        try:
            transactions = r.json()
        except ValueError:
            transactions = {}
        transaction_list = []
        if len(transactions) != 0:
            for t in transactions:
                if t['vendorId'] == vendor_id:
                    transaction_list.append(Transaction(order_id=t['orderId'], is_deal=t['isDeal'], quantity=t['quantity'], unit_price=t['unitPrice'],
                                                        deal_id=t['dealId'], discount=t['dealDiscount'], item_name=t['items']))
        return transaction_list
