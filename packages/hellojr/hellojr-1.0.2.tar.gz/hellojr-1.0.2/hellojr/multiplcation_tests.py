from unittest import TestCase

from .multiplication import multiply


class MultiplicationTests(TestCase):
    def test_multiplication_small(self):
        """
        Ensure that small integers can be multiplied together.
        """
        self.assertEquals(multiply(2, 2), 4)

    def test_multiplication_large(self):
        """
        Ensure that large integers can be multiplied together.
        """
        self.assertEquals(multiply(999999, 999999), 999998000001)
