import requests
from config import PRODUCT_URL
from config import ID_FIELD


class ProductDao(object):
    @staticmethod
    def get_product_name(prod_ids):
        if len(prod_ids) == 0 or prod_ids is None:
            return ''

        r = requests.get(PRODUCT_URL + '/' + prod_ids[0])
        try:
            prod = r.json()
        except ValueError:
            print "Encountered error. No product found."
            return ''
        return prod['prodName']

    @staticmethod
    def get_all_products_for_vendor(vendor_id):
        param = {"vendorId": vendor_id}
        r = requests.get(PRODUCT_URL, params=param)
        products = r.json()
        return products

    @staticmethod
    def post_product(product):
        r = requests.post(PRODUCT_URL, data=product)
        print r

    @staticmethod
    def get_product(vendorId, productName):
        print vendorId, productName
        params = {"vendorId": vendorId, "prodName": productName}
        r = requests.get(PRODUCT_URL, params=params)
        print r
        products = r.json()

        if len(products) == 0 or products is None:
            print "No products with name and vendorId found"

        print products
        product = products[0]
        pid = product[ID_FIELD]
        return pid, product

    @staticmethod
    def delete_product(vendorId, product):
        print vendorId, product.name
        params = {"vendorId": vendorId, "prodName": product.name}
        r = requests.get(PRODUCT_URL, params=params)
        try:
            products = r.json()
            product_id = products[0][ID_FIELD]
            r = requests.delete(PRODUCT_URL + '/' + product_id)
            print r
        except:
            print "No such products found in database"
