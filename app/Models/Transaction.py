__author__ = 'suvir'

class Transaction(object):
    def __init__(self, payment_type,date,tax,total,deal_id,discount):
        self.payment_type = payment_type
        self.date = date
        self.tax = tax
        self.total = total
        self.deal_id = deal_id
        self.discount = discount

