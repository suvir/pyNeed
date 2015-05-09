__author__ = 'Petter'
import unittest
from app import app
from flask_testing import TestCase

class MyTest(TestCase):

    render_templates = False

    def create_app(self):
        app.config['TESTING'] = True
        return app

    def test_login(self):
        response = self.client.get("/login")
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


if __name__ == '__main__':
    unittest.main()