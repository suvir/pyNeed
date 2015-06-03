__author__ = 'suvir'


class Deal(object):
    def __init__(self, name, price, discount, category, expiry_date, coupon_code, product_name):
        self.name = name
        self.price = price
        self.discount = discount
        self.category = category
        self.expiry_date = expiry_date
        self.coupon_code = coupon_code
        self.product_name = product_name

    def to_json(self, vendor_name, vendor_id, product_list_json):
        deal_json = {}
        deal_json['deal_name'] = self.name
        deal_json['vendor_name'] = vendor_name
        deal_json['vendorID'] = vendor_id
        deal_json['type'] = self.category
        deal_json['price'] = str(self.price)
        deal_json['discount'] = str(self.discount)
        deal_json['expire'] = self.expiry_date
        deal_json['coupon_code'] = self.coupon_code
        deal_json['item_sell'] = product_list_json
        return deal_json
