import os
import requests
import json


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

        # Tries to get Tiny ERP's token from environment variable
        TINY_TOKEN_KEY = os.environ.get('TINY_TOKEN_KEY', None)
        if TINY_TOKEN_KEY is None:
            raise APIKeyMissingError(
                'Tiny ERP Token key not found. '
                'Check if it is defined as an environment variable.'
            )

        # Sets Tiny ERP's token
        self.token = TINY_TOKEN_KEY
        # Defines return format, JSON or XML
        self.format = format
        # Sets requests timeout to 10 seconds
        self.timeout = 10
        self.products = []

    def _url(self, url):
        """ Given a url path, returns a complete url to make the API call """
        return f'https://api.tiny.com.br/api2/{url}.php'

    def create_product(self, sequencia=1, situacao='A', tipo='P', **kwargs):
        """
        Creates a product's information dict
        Sets default values of the product to:
        Sequência = 1
        Situação =  'Aprovado'
        Tipo = 'Produto'
        """
        kwargs['sequencia'] = sequencia
        kwargs['situacao'] = situacao
        kwargs['tipo'] = tipo
        kwargs['origem'] = '2'
        return {'produto': kwargs}

    def get_payload(self, **kwargs):
        """ Returns dictionary of required data to make the API call """
        kwargs['token'] = self.token
        kwargs['formato'] = self.format
        return kwargs

    def get_products_payload(self, **kwargs):
        """ Returns dictionary of required data to make the API call """
        kwargs['token'] = self.token
        kwargs['formato'] = self.format
        kwargs['produto'] = {'produtos': self.products}
        return kwargs

    def search_product(self, product):
        """
        Search for a single or multiple products using a string or int
        Returns result(s) as dict
        """
        payload = self.get_payload(pesquisa=product)
        path = self._url('produtos.pesquisa')
        return requests.get(path, params=payload, timeout=self.timeout)

    def get_product(self, id):
        """
        Returns product data as dict from a product id
        Expects id as integer
        """
        payload = self.get_payload(id=id)
        path = self._url('produto.obter')
        return requests.get(path, data=json.dumps(payload), timeout=self.timeout)

    def add_product(self, product):
        """ Adds a product to ERP """
        pass

    def change_product(self, codigo, unidade, preco, tags):
        """
        Changes an existing product from ERP
        The codigo argument is equal to the SKU value in Tiny
        Use dots instead of commas in preco, must be a float type
        tags must be an array of strings containing tag IDs

        Tiny ERP accepts requests as arguments
        It does not work with requests with json argument
        Use requests with data argument
        Requests does not accept nested json,
        so convert nested dicts into json before sending the payload
        """
        product = self.create_product(
                        codigo=codigo,
                        unidade=unidade,
                        preco=preco,
                        tags=tags,
        )
        # self.products.append(product)
        payload = self.get_payload(produto=json.dumps({'produtos': [product]}))
        # payload = self.get_products_payload()
        path = self._url('produto.alterar')
        try:
            r = requests.post(path, data=payload, timeout=self.timeout)
            breakpoint()
            r.raise_for_status()
        except requests.exceptions.HTTPError as err:
            raise SystemExit(err)
        return r

    def get_product_tags(self, id):
        """ Returns all tags from a product """
        payload = self.get_payload(id=id)
        path = self._url('produto.obter.tags')
        try:
            r = requests.get(path, params=payload, timeout=self.timeout)
            r.raise_for_status()
        except requests.exceptions.HTTPError as err:
            raise SystemExit(err)
        return r.json()

    def search_tags(self, pesquisa, idGrupo=None, pagina=None):
        """ Search tags from a pesquisa parameter """
        payload = self.get_payload(pesquisa=pesquisa)
        path = self._url('tag.pesquisa')
        try:
            r = requests.get(path, params=payload, timeout=self.timeout)
            r.raise_for_status()
        except requests.exceptions.HTTPError as err:
            raise SystemExit(err)
        return r.json()
