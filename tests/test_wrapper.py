import os
import sys
import unittest
from unittest.mock import Mock, patch
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
from wrapper import Tiny


class TestWrapper(unittest.TestCase):

    def setUp(self):
        self.app = Tiny()

    def log_request(self, id):
        response_mock = Mock()
        response_mock.status_code = 200
        response_mock.json.return_value = {
            'retorno': {
                'status': 'OK',
                'produto': {
                    'id': id,
                }
            }
        }

    def test_initialization(self):
        """ Test if initialization variables are correct """
        self.assertEqual(self.app.token, os.environ['TINY_TOKEN_KEY'])
        self.assertEqual(self.app.format, 'JSON')

    def test_url_builder(self):
        self.assertEqual(self.app._url('product.add'), 'https://api.tiny.com.br/api2/product.add.php')

    @patch('wrapper.requests')
    def test_get_product(self):
        """ Tests API call to get a product information  """

        # Test product id
        product_id = '550949323'

        # Tries to get a test product with its id
        product_instance = self.app.get_product(product_id)

        self.assertEqual(product_instance.status_code, 200)
        self.assertIsInstance(product_instance.json(), dict)
        response = product_instance.json()
        self.assertEqual(response['retorno']['status'], 'OK')
        self.assertEqual(response['retorno']['produto']['id'], product_id)

    def test_search_product(self):
        """ Tests API call to search for a product name or code  """

        # Test product name
        product_name = 'Selim Brooks C17 Cambium natural para teste'
        # Tries to get a test product with its name
        product_instance = self.app.search_product(product_name)

        # Use mock response
        requests.post.side_effect = self.log_request

        self.assertEqual(product_instance.status_code, 200)
        self.assertIsInstance(product_instance.json(), dict)
        response = product_instance.json()
        self.assertEqual(response['retorno']['status'], 'OK')
        self.assertEqual(response['retorno']['produtos'][0]['produto']['nome'], product_name)

    def test_change_product(self):
        """ Tests changes in a product """
        pass


if __name__ == '__main__':
    unittest.main()
