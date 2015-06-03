__author__ = 'suvir'

from VendorManager import VendorManager
from TransactionDao import TransactionDao

class TransactionManager(object):
    @staticmethod
    def get_all_transactions_for_vendor(vendor_email):
        vendor_id, vendor = VendorManager.get_vendor(email=vendor_email)
        transaction_list = TransactionDao.get_all_transactions_for_vendor(vendor_id)
        return transaction_list