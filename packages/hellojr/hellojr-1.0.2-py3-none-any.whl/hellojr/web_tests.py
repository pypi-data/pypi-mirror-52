from unittest import TestCase

from .web import app


def client():
    """
    Simple testing client for Flask
    """
    app.testing = True
    return app.test_client()


class WebTests(TestCase):
    def setUp(self):
        self.client = client()

    def test_add_view_valid_arguments(self):
        """
        Ensure that the add view can add valid integers together.
        """
        result = self.client.get('/add/5/6')
        self.assertEquals(result.status_code, 200)
        self.assertEquals(b'11', result.data)

    def test_add_view_invalid_arguments(self):
        """
        Ensure that the add view returns an error when invalid arguments are provided.
        """
        result = self.client.get('/add/5/hello')
        self.assertEquals(result.status_code, 404)

    def test_multiply_view_valid_arguments(self):
        """
        Ensure that the multiply view can multiply valid integers together.
        """
        result = self.client.get('/multiply/5/100')
        self.assertEquals(result.status_code, 200)
        self.assertEquals(b'500', result.data)

    def test_multiply_view_invalid_arguments(self):
        """
        Ensure that the multiply view returns an error when invalid arguments are provided.
        """
        result = self.client.get('/multiply/5/hello')
        self.assertEquals(result.status_code, 404)
