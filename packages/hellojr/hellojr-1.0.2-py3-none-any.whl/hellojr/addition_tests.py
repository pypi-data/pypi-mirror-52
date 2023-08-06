from unittest import TestCase

from .addition import add


class AdditionTests(TestCase):
    def test_addition_small(self):
        """
        Ensure that small integers can be added together.
        """
        self.assertEquals(add(1, 1), 2)

    def test_addition_large(self):
        """
        Ensure that large integers can be added together.
        """
        self.assertEquals(add(999999, 999999), 1999998)
