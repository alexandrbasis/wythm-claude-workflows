import unittest
from service import get_customer

class ServiceTests(unittest.TestCase):
    def test_tenant_isolation(self):
        self.assertIsNone(get_customer([{"tenant_id":"a","id":"1"}],"b","1"))
