# -*- coding:utf-8 -*-
import unittest

class FunctionalTests(unittest.TestCase):
    def setUp(self):
        from demo.main import main
        app = main({})
        from webtest import TestApp
        self.testapp = TestApp(app)

    def tearDown(self):
        from demo.main import tear_down
        tear_down()

    def test_count_of_data(self):
        _response = self.testapp.get('/api/users', status=200)
        prev_count = len(_response.json["data"])

        response = self.testapp.post('/api/users', {"name": "*new user*"}, status=200)
        self.assertEqual(response.json["status"], True)

        _response = self.testapp.get('/api/users', status=200)
        self.assertEqual(len(_response.json["data"]), prev_count+1) #adhoc

    def test_one_model_action(self):
        ## create
        response = self.testapp.post('/api/users', {"name": "*new user*"}, status=200)
        self.assertEqual(response.json["status"], True)

        ## detail
        response = self.testapp.get('/api/users/1', status=200)
        self.assertEqual(response.json["status"], True)
        self.assertEqual(response.json["data"]["id"], 1)

        ## update
        response = self.testapp.post('/api/users/1', {"name": "*updated*"}, status=200)
        self.assertEqual(response.json["status"], True)

        ## detail (after updated)
        _response = self.testapp.get('/api/users/1', status=200)
        self.assertEqual(_response.json["data"]["name"], "*updated*")

        ## delete
        response = self.testapp.delete('/api/users/1', status=200)
        self.assertEqual(response.json["status"], True)

        ## detail (after deleted)
        self.testapp.get('/api/users/1', status=404)

    def test_validation_error__unique(self):
        ## create
        response = self.testapp.post('/api/users', {"name": "*new user*"}, status=200)
        self.assertEqual(response.json["status"], True)

        ## create with same name
        response = self.testapp.post('/api/users', {"name": "*new user*"}, status=200)
        self.assertEqual(response.json["status"], False)
        self.assertEqual(response.json["message"], {'name': ['name: *new user* is conflict.']})

        ## create
        response = self.testapp.post('/api/users', {"name": "another"}, status=200)
        self.assertEqual(response.json["status"], True)

        ## create with same name
        response = self.testapp.post('/api/users/1', {"name": "another"}, status=200)
        self.assertEqual(response.json["status"], False)
        self.assertEqual(response.json["message"], {'name': ['name: another is conflict.']})



