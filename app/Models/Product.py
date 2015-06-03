__author__ = 'suvir'


class Product(object):
    def __init__(self, id=None, name=None, description=None, price=None):
        self.id = id
        self.name = name
        self.description = description
        self.price = price

    def to_json(self, vendorId):
        prod_json = {}
        prod_json['prodName'] = self.name
        prod_json['prodDesc'] = self.description
        prod_json['price'] = self.price
        prod_json['quantity'] = 1
        prod_json['category'] = "perishable"
        prod_json['vendorId'] = vendorId
        return prod_json
