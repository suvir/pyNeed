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
        self.assertRedirects(response,"/login")

    def test_catalog_with_email_in_session(self):
        with self.client as c:
            with c.session_transaction() as sess:
                sess['logged'] = True
                sess['email'] = 'pedasda@pe.com'
            response = c.get('/catalog')
        self.assertRedirects(response,"/login")

    def test_deal_without_valid_email(self):
        response = self.client.get("/deals")
        self.assertRedirects(response,"/login")

    def test_deals_with_email_in_session(self):
        with self.client as c:
            with c.session_transaction() as sess:
                sess['logged'] = True
                sess['email'] = 'pe@pe.com'
            response = c.get('/deals')
        self.assertRedirects(response,"/login")

    def test_index_with_email_in_session_invalid_email(self):
        with self.client as c:
            with c.session_transaction() as sess:
                sess['logged'] = True
                sess['email'] = 'pe@pe.com'
            response = c.get('/index')
        self.assertRedirects(response,"/login")

    def test_index_with_email_in_session_valid_email(self):
        with self.client as c:
            with c.session_transaction() as sess:
                sess['logged'] = True
                sess['email'] = 'petter@petter.com'
            response = c.get('/index')
        print response
        self.assert200(response)


    def test_api_vendor_types(self):
        response = self.client.get("/api/vendor/types")
        self.assert200(response)
        self.assertTrue(is_json(response.data))

    def test_api_vendor_types_with_invalid_id(self):
        response = self.client.get("/api/vendor/type/0001234invalid")
        self.assert404(response)
        self.assertTrue(is_json(response.data))

    def test_api_vendor_types_with_valid_id(self):
        response = self.client.get("/api/vendor/type/0001234invalid")#todo: Maintain valid id when changing to team 10 database
        self.assert404(response)
        self.assertTrue(is_json(response.data))

    def test_api_vendor_catalog_with_valid_id(self):
        response = self.client.get("/api/vendor/catalog/555579fb7d81a62b0005ded2")#todo: Maintain valid id when changing to team 10 database
        self.assert200(response)
        self.assertTrue(is_json(response.data))

    def test_api_vendor_catalog_with_invalid_id(self):
        response = self.client.get("/api/vendor/catalog/555679fb7d81a62b0005ded2")
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