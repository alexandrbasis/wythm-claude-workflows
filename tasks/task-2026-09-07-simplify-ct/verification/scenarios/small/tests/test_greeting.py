import unittest
from greeting import greet

class GreetingTests(unittest.TestCase):
    def test_normal_name(self):
        self.assertEqual(greet("Alex"), "Hello, Alex!")
