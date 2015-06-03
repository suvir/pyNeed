__author__ = 'suvir'
import requests
from Transaction import Transaction
from config import GET_TRANSACTIONS_URL


class TransactionDao(object):
    @staticmethod
    def get_all_transactions_for_vendor(vendor_id):
        params = {}
        r = requests.get(GET_TRANSACTIONS_URL, params=params)
        try:
            transactions = r.json()
        except ValueError:
            transactions = {}
        transaction_list = []
        if len(transactions) != 0:
            for t in transactions:
                if t['vendorId'] == vendor_id:
                    transaction_list.append(Transaction(payment_type=t['payment_type'], tax=t['tax'], total=t['total'],
                                                        deal_id=t['deal_id'], discount=t['discount']))
        return transaction_list
