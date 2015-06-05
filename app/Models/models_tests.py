__author__ = 'Petter'


import unittest
import json
from Deal import Deal
from Product import Product
from Vendor import Vendor
class TestDeal(unittest.TestCase):

  def test_create_deal(self):
      d = Deal(name="test", item_list="test,test",
         coupon_code="test", price="test", discount="test", category="test",
         expiry_date="test", id="test")
      self.assertEqual(d.name, "test")
      self.assertEqual(d.item_list, ['test', 'test'])
      self.assertEqual(d.coupon_code, "test")
      self.assertEqual(d.price, "test")
      self.assertEqual(d.discount, "test")
      self.assertEqual(d.category, "test")
      self.assertEqual(d.expiry_date, "test")
      self.assertEqual(d.id, "test")

  def test_jsonify_deal(self):
      d = Deal(name="test", item_list="test,test",
         coupon_code="test", price=12, discount=23, category="test",
         expiry_date="test", id="test")
      encoded_json = d.to_json("test","test")
      print encoded_json
      self.assertEqual(encoded_json['vendorID'],"test")
      self.assertEqual(encoded_json['coupon_code'],"test")
      self.assertEqual(encoded_json['expire'],"test")
      self.assertEqual(encoded_json['deal_name'],"test")
      self.assertEqual(encoded_json['vendor_name'],"test")
      self.assertEqual(encoded_json['type'],"test")
      self.assertEqual(encoded_json['price'],"12")
      self.assertEqual(encoded_json['discount'],"23")
      self.assertEqual(encoded_json['item_sell'],'["test", "test"]')

  def test_create_product(self):
      p = Product(id ="test", name = "test", description = "test",price = "test")
      self.assertEqual(p.name, "test")
      self.assertEqual(p.id, "test")
      self.assertEqual(p.price, "test")
      self.assertEqual(p.description, "test")

  def test_jsonify_product(self):
      p = Product(id ="test", name = "test", description = "test",price = "test")
      encoded_json = p.to_json("test")
      print encoded_json
      self.assertEqual(encoded_json['prodName'],"test")
      self.assertEqual(encoded_json['prodDesc'],"test")
      self.assertEqual(encoded_json['price'],"test")
      self.assertEqual(encoded_json['quantity'],1)
      self.assertEqual(encoded_json['category'],"perishable")
      self.assertEqual(encoded_json['vendorId'],"test")

  def test_create_vendor(self):
      v = Vendor(name="test", description="test",
         email="test", category="test", address="test", latitude="test",
         longitude="test", phone="test",state="test",city="test",
         pwdhash="test")
      self.assertEqual(v.name, "test")
      self.assertEqual(v.description, "test")
      self.assertEqual(v.email, "test")
      self.assertEqual(v.category, "test")
      self.assertEqual(v.address, "test")
      self.assertEqual(v.latitude, "test")
      self.assertEqual(v.longitude, "test")
      self.assertEqual(v.phone, "test")
      self.assertEqual(v.state, "test")
      self.assertEqual(v.city, "test")
      self.assertEqual(v.pwdhash, "test")

  def test_jsonify_vendor(self):
      v = Vendor(name="test", description="test",
         email="test", category="test", address="test", latitude="test",
         longitude="test", phone="test",state="test",city="test",
         pwdhash="test")
      encoded_json = v.to_json()
      print encoded_json
      self.assertEqual(encoded_json['name'],"test")
      self.assertEqual(encoded_json['description'],"test")
      self.assertEqual(encoded_json['email'],"test")
      self.assertEqual(encoded_json['type'],"test")
      self.assertEqual(encoded_json['coordinates'],["test","test"])
      self.assertEqual(encoded_json['phoneNumber'],"test")
      self.assertEqual(encoded_json['state'],"test")
      self.assertEqual(encoded_json['city'],"test")
      self.assertEqual(encoded_json['password'],"test")
      self.assertEqual(encoded_json['notiPref'],"email")






if __name__ == '__main__':
    unittest.main()