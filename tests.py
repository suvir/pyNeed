__author__ = 'Petter'
import unittest
import json
from app import app
from flask_testing import TestCase
from app.forms import SignupForm
from coverage import coverage
cov = coverage(branch=True, omit=['flask/*', 'tests.py'])
cov.start()

class MyTest(TestCase):

    render_templates = False

    def create_app(self):
        app.config['TESTING'] = True
        return app

    def test_login(self):
        response = self.client.get("/index")
        self.assert200(response)

    def test_index(self):
        response = self.client.get("/index")
        self.assert200(response)

    def test_signup(self):
        response = self.client.get("/signup")
        self.assert200(response)

    def test_logout(self):
        response = self.client.get("/logout")
        self.assertRedirects(response,"/login")

    def test_profile_without_valid_email(self):
        response = self.client.get("/profile")
        self.assertRedirects(response,"/login")

    def test_profile_with_email_in_session_invalid_email(self):
        with self.client as c:
            with c.session_transaction() as sess:
                sess['logged'] = True
                sess['email'] = 'peefwf@pe.com'
            response = c.get('/profile')
        self.assertRedirects(response,"/login")

    def test_catalog_without_valid_email(self):
        response = self.client.get("/catalog")
        self.assertRedirects(response,"/index")

    def test_catalog_with_invalid_email_in_session(self):
        with self.client as c:
            with c.session_transaction() as sess:
                sess['logged'] = True
                sess['email'] = 'pedasda@pe.com'
            response = c.get('/catalog')
        self.assertRedirects(response,"/index")

    def test_catalog_with_valid_email_in_session(self):
        with self.client as c:
            with c.session_transaction() as sess:
                sess['logged'] = True
                sess['email'] = 'per@per.com'
            response = c.get('/catalog')
        self.assert200(response)

    def test_deal_without_valid_email(self):
        response = self.client.get("/deals")
        self.assertRedirects(response,"/index")

    def test_deals_with_email_in_session(self):
        with self.client as c:
            with c.session_transaction() as sess:
                sess['logged'] = True
                sess['email'] = 'per@per.com'
            response = c.get('/deals')
        self.assert200(response)

    def test_index_with_email_in_session_invalid_email(self):
        with self.client as c:
            with c.session_transaction() as sess:
                sess['logged'] = True
                sess['email'] = 'pe@pe.com'
            response = c.get('/index')
        self.assert200(response)

    def test_index_with_email_in_session_valid_email(self):
        with self.client as c:
            with c.session_transaction() as sess:
                sess['logged'] = True
                sess['email'] = 'per@per.com'
            response = c.get('/index')
        print response
        self.assert200(response)

    def test_transactions_with_email_in_session_invalid_email(self):
        with self.client as c:
            with c.session_transaction() as sess:
                sess['logged'] = True
                sess['email'] = 'perqweqwe@perqweqwe.com'
            response = c.get('/transactions')
        self.assert404(response)

    def test_transactions_with_email_in_session_valid_email(self):
        with self.client as c:
            with c.session_transaction() as sess:
                sess['logged'] = True
                sess['email'] = 'per@per.com'
            response = c.get('/transactions')
        print response
        self.assert200(response)

    def test_transactions_without_email_in_session(self):
        response = self.client.get('/transactions')
        print response
        self.assertRedirects(response,"/index")

    def test_api_vendor_types(self):
        response = self.client.get("/api/vendor/types")
        self.assert200(response)
        self.assertTrue(is_json(response.data))

    def test_api_vendor_types_with_invalid_id(self):
        response = self.client.get("/api/vendor/type/0001234invalid")
        self.assert404(response)
        self.assertTrue(is_json(response.data))

    def test_api_vendor_types_with_valid_id(self):
        response = self.client.get("/api/vendor/type/556fca8058d4062b006e6ca2")#todo: Maintain valid id when changing to team 10 database
        self.assert200(response)
        self.assertTrue(is_json(response.data))

    def test_api_vendor_types_with_invalid_id_valid_bson(self):
        response = self.client.get("/api/vendor/type/556fca8058d4062b068e6ca2")#todo: Maintain invalid id but valif bson when changing to team 10 database
        self.assert404(response)
        self.assertTrue(is_json(response.data))

    def test_api_vendor_catalog_with_valid_id(self):
        response = self.client.get("/api/vendor/catalog/556fca8058d4062b006e6ca2")#todo: Maintain valid id when changing to team 10 database
        self.assert200(response)
        self.assertTrue(is_json(response.data))

    def test_api_vendor_catalog_with_invalid_id_valid_bson(self):
        response = self.client.get("/api/vendor/catalog/555679fb7d81a62b0005ded2")
        self.assert404(response)
        self.assertTrue(is_json(response.data))

    def test_api_vendor_catalog_with_invalid_id(self):
        response = self.client.get("/api/vendor/catalog/555679fb7dasdasd")
        self.assert404(response)
        self.assertTrue(is_json(response.data))

    def test_api_all_vendors(self):
        response = self.client.get("/api/vendors/")
        self.assert200(response)
        self.assertTrue(is_json(response.data))

    def test_api_vendor_notify_with_valid_id(self):
        response = self.client.get("/api/vendor/notify?vendorId=556fe73f58d4062b006e6ca4&transactionId=123&message=hey")#todo: Maintain valid id when changing to team 10 database
        self.assert200(response)
        self.assertTrue(is_json(response.data))

    def test_api_vendor_notify_with_invalid_id_valid_bson(self):
        response = self.client.get("/api/vendor/notify?vendorId=556fe73f58d4081b006e6ca4&transactionId=123&message=hey")
        self.assert404(response)
        self.assertTrue(is_json(response.data))

    def test_api_vendor_notify_with_invalid_id(self):
        response = self.client.get("/api/vendor/notify?vendorId=556fe7asdasd&transactionId=123&message=hey")
        self.assert404(response)
        self.assertTrue(is_json(response.data))




def is_json(myjson):
  try:
    json_object = json.loads(myjson)
  except ValueError, e:
    return False
  return True



if __name__ == '__main__':
    try:
        unittest.main()
    except:
        pass
    cov.stop()
    cov.save()
    print "\n\nCoverage Report:\n"
    cov.report()
    cov.html_report(directory='tmp/coverage')
    cov.erase()