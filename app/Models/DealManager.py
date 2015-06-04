import json
from Deal import Deal
from DealDao import DealDao
from ProductManager import ProductManager


class DealManager(object):
    @staticmethod
    def create_deal(deal, item_list):
        d = Deal(name=deal['dealName'], item_list=item_list,
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
        deal_json = deal.to_json(vendor_name, vendor_id)
        return deal_json

    @staticmethod
    def parse_deal_list_multidict(f):
        deals = []
        if 'add_qty' in f and 'add_coupon_code' in f and 'add_item_list' in f and 'add_price' in f and 'add_expiry_date' in f and 'add_deal_type' in f and 'add_discount' in f:
            if len(f['add_qty']) > 0 and len(f['add_item_list']) > 0 and len(f['add_coupon_code']) > 0 and len(
                    f['add_price']) > 0 and len(f['add_expiry_date']) > 0 and len(f['add_deal_type']) > 0 and len(
                f['add_discount']) > 0:
                try:
                    deal_price = float(f['add_price'])
                    deal_discount = float(f['add_discount'])
                except:
                    deal_price = 0.0
                    deal_discount = 0.0
                deals.append(Deal(name=f['add_qty'], price=deal_price, discount=deal_discount,
                                category=f['add_deal_type'], expiry_date=f['add_expiry_date'],
                                coupon_code=f['add_coupon_code'], item_list = f['add_item_list']))

        deal_counter = 1
        next_item_name = 'qty' + str(deal_counter)
        #next_item_prod_name = 'prod_name' + str(deal_counter)
        #next_item_desc = 'name' + str(deal_counter)
        next_item_price = 'price' + str(deal_counter)
        next_item_discount = 'discount' + str(deal_counter)
        next_item_expiry_date = 'expiry_date' + str(deal_counter)
        next_item_category = 'deal_type' + str(deal_counter)
        next_item_coupon_code = 'coupon_code' + str(deal_counter)
        next_item_itemlist = 'item_list' + str(deal_counter)

        while next_item_name in f and next_item_itemlist in f and next_item_price in f:
            if len(f[next_item_name]) > 0 and len(f[next_item_itemlist]) > 0 and len(f[next_item_desc]) > 0 and len(
                    f[next_item_price]) > 0 and len(f[next_item_discount]) > 0 and len(
                f[next_item_category]) > 0 and len(f[next_item_expiry_date]) > 0:
                try:
                    deal_price = float(f[next_item_price])
                    deal_discount = float(f[next_item_discount])
                except:
                    deal_price = 0
                    deal_discount = 0
                deals.append(
                    Deal(name=f[next_item_name], price=deal_price, discount=deal_discount,
                         category=f[next_item_category],expiry_date=f[next_item_expiry_date],
                         coupon_code = f[next_item_coupon_code], item_list = f[next_item_itemlist]))

            deal_counter += 1
            next_item_name = 'qty' + str(deal_counter)
            #next_item_prod_name = 'prod_name' + str(deal_counter)
            next_item_desc = 'name' + str(deal_counter)
            next_item_price = 'price' + str(deal_counter)
            next_item_discount = 'discount' + str(deal_counter)
            next_item_expiry_date = 'expiry_date' + str(deal_counter)
            next_item_category = 'deal_type' + str(deal_counter)
            next_item_coupon_code = 'coupon_code' + str(deal_counter)
            next_item_itemlist = 'item_list' + str(deal_counter)

        return deals
