# -*- coding:utf-8 -*-

import unittest

class AddPickTests(unittest.TestCase):
    def _getTarget(self):
        from block.komet.pyramid.validation import with_pick
        return with_pick

    def test_it(self):
        decorator = self._getTarget()
        input_data = object()
        DBSession = object()
        login_user = object()
        @decorator(positionals=["session"], optionals=["id", ("login_user", "user")])
        def validation(data, session, id=None, user=None):
            self.assertEqual(data, input_data)
            self.assertEqual(session, DBSession)
            self.assertEqual(id, 1)
            self.assertEqual(user, login_user)

        self.assertTrue(hasattr(validation, "pick"))
        validation.pick(validation, input_data, {"id": 1, "session": DBSession, "login_user": login_user})


class ValidationQueueTests(unittest.TestCase):
    def _getTarget(self):
        from block.komet.pyramid.validation import ValidationQueue
        return ValidationQueue

    def _makeOne(self, *args, **kwargs):
        return self._getTarget()(*args, **kwargs)

    def test_pick__empty(self):
        target = self._makeOne()
        def validation(data):
            raise Exception("error!")
        result = target.get_pick_from_validtion(validation, None)
        self.assertIsNone(result)

    def test_pick__has_pick__byhand(self):
        target = self._makeOne()
        def use_db_validation(data, session):
            raise Exception("error!")
        use_db_validation.pick = lambda cb, data, extra: cb(data, session=extra["session"])
        result = target.get_pick_from_validtion(use_db_validation, None)
        self.assertEqual(result, use_db_validation.pick)

    def test_pick__passing_pick(self):
        target = self._makeOne()
        def use_db_validation(data, session):
            raise Exception("error!")
        pick = object()
        result = target.get_pick_from_validtion(use_db_validation, pick=pick)
        self.assertEqual(result, pick)

    def test_normalize__without_pick(self):
        target = self._makeOne()
        def use_db_validation(data, session):
            raise Exception("error!")
        result = target.normalize(use_db_validation, None)
        self.assertEqual(result.__name__, "validation_simple") #xxx:

    def test_normalize__with_pick(self):
        target = self._makeOne()
        def use_db_validation(data, session):
            raise Exception("error!")
        pick = object()
        result = target.normalize(use_db_validation, pick)
        self.assertEqual(result.__name__, "validation_with_extra") #xxx:

    def test_it(self):
        from block.komet.pyramid.validation import with_pick
        target = self._makeOne()
        DBSession = object()
        params = {"group_id": 100}

        @with_pick(["session"])
        def use_db_validation(data, session):
            self.assertEqual(data, params)
            self.assertEqual(session, DBSession)

        @with_pick(optionals=["user"])
        def login_user__same_group_id(data, user=None):
            if user is None:
                raise Exception("test failed")
            self.assertEqual(user.group_id, data["group_id"])

        target.add("all", use_db_validation)
        target.add("group_id", login_user__same_group_id)

        class login_user:
            group_id = 100

        for name, validation in target({"user": login_user, "session": DBSession}):
            validation(params)

if __name__ == '__main__':
    unittest.main()
