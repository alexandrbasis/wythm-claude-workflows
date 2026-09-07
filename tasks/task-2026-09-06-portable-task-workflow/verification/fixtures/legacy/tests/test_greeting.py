import unittest
from greeting import greet

class GreetingTests(unittest.TestCase):
    def test_regular_name(self):
        self.assertEqual(greet("Alex"), "Hello, Alex!")

    def test_trims_outer_whitespace_and_preserves_inner_spaces(self):
        self.assertEqual(greet("  Alex Basis  "), "Hello, Alex Basis!")
