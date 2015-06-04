__author__ = 'suvir'

class Transaction(object):
    def __init__(self, order_id, item_name, is_deal, quantity, unit_price, deal_id, discount):
        self.order_id = order_id
        self.is_deal = is_deal
        self.item_name = item_name
        try:
            self.total = (unit_price-discount)*quantity
        except TypeError:
            self.total = unit_price*quantity
        self.deal_id = deal_id
        self.discount = discount

