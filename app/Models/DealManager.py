import json
from Deal import Deal
from DealDao import DealDao
from ProductManager import ProductManager


class DealManager(object):
    @staticmethod
    def create_deal(deal, product_name):
        d = Deal(name=deal['dealName'], product_name=product_name,
                 coupon_code=deal['couponCode'], price=deal['price'], discount=deal['discount'], category=deal['type'],
                 expiry_date=deal['expireDate'])
        return d

    @staticmethod
    def get_all_deals_for_vendor(vendor_id):
        deals = DealDao.get_all_deals_for_vendor(vendor_id)
        return deals

    @staticmethod
    def post_deal(deal, vendor_name, vendor_id):
        deal_json = DealManager.transform_to_json(deal, vendor_name, vendor_id)
        r = DealDao.post_deal(deal_json)
        print r

    @staticmethod
    def post_deals_many(deals, vendor_id, vendor_name):
        for deal in deals:
            DealManager.post_deal(deal, vendor_name, vendor_id)

    @staticmethod
    def get_deal(vendor_id, deal_name):
        deal_id, deal = DealDao.get_deal(vendor_id, deal_name)
        return deal_id, deal

    @staticmethod
    def delete_deal(vendor_id, deal, vendor_name):
        DealDao.delete_deal(vendor_id, deal, vendor_name)

    @staticmethod
    def transform_to_json(deal, vendor_name, vendor_id):
        products = []
        prod_id, product = ProductManager.get_product(vendor_id, deal.product_name)
        products.append(str(prod_id))
        item_sell_json = json.dumps(products)
        deal_json = deal.to_json(vendor_name, vendor_id, item_sell_json)
        return deal_json

    @staticmethod
    def parse_deal_list_multidict(f):
        deals = []
        if 'add_qty' in f and 'add_prod_name' in f and 'add_name' in f and 'add_price' in f and 'add_expiry_date' in f and 'add_deal_type' in f and 'add_discount' in f:
            if len(f['add_qty']) > 0 and len(f['add_prod_name']) > 0 and len(f['add_name']) > 0 and len(
                    f['add_price']) > 0 and len(f['add_expiry_date']) > 0 and len(f['add_deal_type']) > 0 and len(
                f['add_discount']) > 0:
                try:
                    deal_price = float(f['add_price'])
                    deal_discount = float(f['add_discount'])
                except:
                    deal_price = 0.0
                    deal_discount = 0.0
                deals.append(Deal(name=f['add_qty'], product_name=f['add_prod_name'], description=f['add_name'],
                                  price=deal_price, discount=deal_discount, category=f['add_deal_type'],
                                  expiry_date=f['add_expiry_date']))

        deal_counter = 1
        next_item_name = 'qty' + str(deal_counter)
        next_item_prod_name = 'prod_name' + str(deal_counter)
        next_item_desc = 'name' + str(deal_counter)
        next_item_price = 'price' + str(deal_counter)
        next_item_discount = 'discount' + str(deal_counter)
        next_item_expiry_date = 'expiry_date' + str(deal_counter)
        next_item_category = 'deal_type' + str(deal_counter)

        while next_item_name in f and next_item_prod_name in f and next_item_desc in f and next_item_price in f:
            if len(f[next_item_name]) > 0 and len(f[next_item_prod_name]) > 0 and len(f[next_item_desc]) > 0 and len(
                    f[next_item_price]) > 0 and len(f[next_item_discount]) > 0 and len(
                f[next_item_category]) > 0 and len(f[next_item_expiry_date]) > 0:
                try:
                    deal_price = float(f[next_item_price])
                    deal_discount = float(f[next_item_discount])
                except:
                    deal_price = 0
                    deal_discount = 0
                deals.append(
                    Deal(name=f[next_item_name], product_name=f[next_item_prod_name], description=f[next_item_desc],
                         price=deal_price, discount=deal_discount, category=f[next_item_category],
                         expiry_date=f[next_item_expiry_date]))

            deal_counter += 1
            next_item_name = 'qty' + str(deal_counter)
            next_item_prod_name = 'prod_name' + str(deal_counter)
            next_item_desc = 'name' + str(deal_counter)
            next_item_price = 'price' + str(deal_counter)
            next_item_discount = 'discount' + str(deal_counter)
            next_item_expiry_date = 'expiry_date' + str(deal_counter)
            next_item_category = 'deal_type' + str(deal_counter)

        return deals
