import threading
import unittest

import httpbin

from curl_requests import PreparedRequest, Request, Response, Session


class TestCommon(unittest.TestCase):
    def test_slots(self):
        # The real `requests` has a lot of attributes that people use.
        # Make sure they don't.
        # Chances are most will be added as @property's, not attributes.
        for cls in [PreparedRequest, Request, Response, Session]:
            with self.assertRaises(AttributeError):
                cls().bogus = 'attributes not allowed'
