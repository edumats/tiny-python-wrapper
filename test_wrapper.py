import os
import unittest
from unittest.mock import patch
import wrapper
import mock_return_values


class TestWrapper(unittest.TestCase):

    def setUp(self):
        self.wrapper = wrapper.Tiny()

    def test_initialization(self):
        """ Test if initialization variables are correct """
        self.assertEqual(self.wrapper.token, os.environ['TINY_TOKEN_KEY'])
        self.assertEqual(self.wrapper.format, 'JSON')

    def test_url_builder(self):
        """ Test if generated url is the expected one """
        self.assertEqual(
            self.wrapper._url('product.add'),
            'https://api.tiny.com.br/api2/product.add.php'
        )

    def test_get_product(self):
        """ Tests getting a product information  """

        # Test product id
        product_id = 550949323

        # Uses Mock to simulate response
        with patch('wrapper.requests') as mock_requests:
            # Mock will return a JSON success response
            mock_requests.return_value = mock_return_values.get_product_success

            # Tries to get a test product with its id
            product_instance = self.wrapper.get_product(product_id)

            # Checks if a dict is returned
            self.assertIsInstance(product_instance, dict)

    def test_search_product(self):
        """ Tests API call to search for a product name or code  """

        # Test product name
        product_name = 'Selim Brooks C17 Cambium natural para teste'

        # Uses Mock to simulate response
        with patch('wrapper.requests') as mock_requests:
            # Mock will return a JSON success response
            mock_requests.return_value = mock_return_values.search_product_success
            # Tries to get a test product with its name
            product_instance = self.wrapper.search_product(product_name)
            self.assertIsInstance(product_instance.json(), dict)

    def test_change_product(self):
        """ Tests changes in a product """
        with patch() as mock_requests:
            mock_requests.return_value = mock_return_values.change_product_success

    def test_update_price(self):
        """ Tests updating a product price """
        pass


if __name__ == '__main__':
    unittest.main()
