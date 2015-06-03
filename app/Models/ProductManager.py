__author__ = 'suvir'
from ProductDao import ProductDao
from Product import Product


class ProductManager(object):
    @staticmethod
    def create_product(prod):
        p = Product(id=prod['_id'], name=prod['prodName'], description=prod['prodDesc'], price=prod['price'])
        return p

    @staticmethod
    def get_product_name(prod_ids):
        products = ProductDao.get_product_name(prod_ids)
        return products

    @staticmethod
    def get_all_products_for_vendor(vendor_id):
        products = ProductDao.get_all_products_for_vendor(vendor_id)
        return products

    @staticmethod
    def post_product(product, vendor_id):
        prod_json = product.to_json(vendor_id)
        ProductDao.post_product(prod_json)

    @staticmethod
    def post_products_many(products, vendor_id):
        for prod in products:
            ProductManager.post_product(prod, vendor_id)

    @staticmethod
    def get_product(vendorId, productName):
        pid, product = ProductDao.get_product(vendorId, productName)
        return pid, product

    @staticmethod
    def delete_product(vendorId, product):
        ProductDao.delete_product(vendorId, product)

    @staticmethod
    def parse_product_catalog_multidict(f):
        products = []
        if 'add_qty' in f and 'add_name' in f:
            if len(f['add_qty']) > 0 and len(f['add_name']) > 0 and len(f['add_price']) > 0:
                products.append(Product(name=f['add_qty'], description=f['add_name'], price=f['add_price']))

        product_counter = 1
        next_item_name = 'qty' + str(product_counter)
        next_item_desc = 'name' + str(product_counter)
        next_item_price = 'price' + str(product_counter)
        while next_item_name in f and next_item_desc in f:
            if len(f[next_item_name]) > 0 and len(f[next_item_desc]) > 0:
                products.append(
                    Product(name=f[next_item_name], description=f[next_item_desc], price=f[next_item_price]))
            product_counter += 1
            next_item_name = 'qty' + str(product_counter)
            next_item_desc = 'name' + str(product_counter)
            next_item_price = 'price' + str(product_counter)
        return products

    @staticmethod
    def parse_product(f):
        product = Product()
        product.name = f['name']
        product.description = f['description']
        return product

    @staticmethod
    def print_product_catalog_multidict(f):
        print "Printing out all received values"
        for key in f:
            for value in f.getlist(key):
                print key, ":", value, type(value)
