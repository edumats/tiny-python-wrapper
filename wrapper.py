import os
import requests


class APIKeyMissingError(Exception):
    pass


class Tiny:
    def __init__(self, format='JSON'):
        """ format can be JSON or XML """
        supported_formats = ['JSON', 'XML']

        if format not in supported_formats:
            raise ValueError(
                f'Invalid format type. Expected one of: {supported_formats}'
            )

        TINY_TOKEN_KEY = os.environ.get('TINY_TOKEN_KEY', None)

        if TINY_TOKEN_KEY is None:
            raise APIKeyMissingError(
                'Tiny ERP Token key not found. '
                'Check if it is defined as an environment variable.'
            )

        self.token = TINY_TOKEN_KEY
        self.format = format

    def _url(self, url):
        """ Given a url path, returns a complete url to make the API call """
        return f'https://api.tiny.com.br/api2/{url}.php'

    def create_product(self, sequencia, nome, ):
        pass

    def get_payload(self, **kwargs):
        """ Returns dictionary of required data to make the API call """
        kwargs['token'] = self.token
        kwargs['formato'] = self.format
        return kwargs

    def search_product(self, product):
        """
        Search for a single or multiple products from a string or int
        Returns result(s) as dict
        """
        payload = self.get_payload(pesquisa=product)
        path = self._url('produtos.pesquisa')
        return requests.post(path, payload)

    def get_product(self, id):
        """
        Returns product data as dict from a product id
        Expects id as integer
        """
        payload = self.get_payload(id=id)
        path = self._url('produto.obter')
        return requests.post(path, payload)

    def add_product(self, product):
        pass

    def change_product(self, product):
        pass

    def get_tags(self, id):
        """ Returns all tags from a product """
        payload = self.get_payload(id=id)
        path = self._url('produto.obter.tags')
        return requests.post(path, payload)
