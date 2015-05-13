__author__ = 'Petter'
import unittest
import json
from app import app
from flask_testing import TestCase

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

    def test_catalog_without_valid_email(self):
        response = self.client.get("/catalog")
        self.assertRedirects(response,"/login")

    def test_index_with_email_in_session(self):
        with self.client as c:
            with c.session_transaction() as sess:
                sess['logged'] = True
                sess['email'] = 'pet@pet.com'
            response = c.get('/index')
        print response
        self.assertRedirects(response,"/login")

    def test_api_vendor_types(self):
        response = self.client.get("/api/vendor/types")
        self.assert200(response)
        self.assertTrue(is_json(response.data))

    def test_api_vendor_types_with_invalid_id(self):
        response = self.client.get("/api/vendor/type/0001234invalid")
        self.assert404(response)
        self.assertTrue(is_json(response.data))

    def test_api_vendor_types_with_valid_id(self):
        response = self.client.get("/api/vendor/type/insertvalidid")#todo: Insert a valid id
        self.assert200(response)
        self.assertTrue(is_json(response.data))

    def test_api_vendor_catalog_with_valid_id(self):
        response = self.client.get("/api/vendor/catalog/insertvalidid")#todo: Insert a valid id
        self.assert200(response)
        self.assertTrue(is_json(response.data))

    def test_api_vendor_catalog_with_invalid_id(self):
        response = self.client.get("/api/vendor/catalog/0001234invalid")
        self.assert404(response)
        self.assertTrue(is_json(response.data))


def is_json(myjson):
  try:
    json_object = json.loads(myjson)
  except ValueError, e:
    return False
  return True



if __name__ == '__main__':
    unittest.main()