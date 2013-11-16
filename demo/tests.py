# -*- coding:utf-8 -*-
import unittest

class FunctionalTests(unittest.TestCase):
    def setUp(self):
        from demo.main import main
        app = main({})
        from webtest import TestApp
        self.testapp = TestApp(app)

    def test_listing(self):
        response = self.testapp.get('/api/users', status=200)
        self.assertEqual(response.json["status"], True)
        self.assertEqual(len(response.json["data"]), 3) #adhoc

    def test_create(self):
        _response = self.testapp.get('/api/users', status=200)
        prev_count = len(_response.json["data"])

        response = self.testapp.post('/api/users', {"name": "*new user*"}, status=200)
        self.assertEqual(response.json["status"], True)

        _response = self.testapp.get('/api/users', status=200)
        self.assertEqual(len(_response.json["data"]), prev_count+1) #adhoc

    def test_detail(self):
        response = self.testapp.get('/api/users/1', status=200)
        self.assertEqual(response.json["status"], True)
        self.assertEqual(response.json["data"]["id"], 1)

    def test_update(self):
        response = self.testapp.post('/api/users/1', {"name": "*updated*"}, status=200)
        self.assertEqual(response.json["status"], True)

        _response = self.testapp.get('/api/users/1', status=200)
        self.assertEqual(_response.json["data"]["name"], "*updated*")

    def test_delete(self):
        response = self.testapp.delete('/api/users/2', status=200)
        self.assertEqual(response.json["status"], True)

        self.testapp.get('/api/users/2', status=404)

