import os
import json
import shutil
from .utils import *


class Env(unittest.TestCase):
    def setUp(self):
        """ Inicia novo objeto em todo os testes """
        self.ufrn_data = ODUFRNDownloader()
        self.test_dir = 'temporary_test_dir'

    def test_can_print_exception(self):
        """ Verifica se uma exceção consegue ser printada no console """
        assert_console(lambda: self.ufrn_data._print_exception(ValueError()))

    def test_can_print_list(self):
        """ Verifica se consegue-se printar informação da lista no console """
        assert_console(
            lambda: self.ufrn_data._print_list(
                "conjuntos de dados", ['discente']
            )
        )

    def test_can_load_list(self):
        """ Verifica se consegue carregar uma lista advinda de requisição """
        self.assertIsInstance(self.ufrn_data._load_list('package_list'), list)

    def test_can_make_dir(self):
        """ Verifica se pode-se criar um diretório """
        self.ufrn_data._make_dir(self.test_dir)
        self.assertTrue(os.path.exists(self.test_dir))
        shutil.rmtree(self.test_dir)

    def test_can_request_get(self):
        """ Verifica se consegue-se realizar requisição get e retornar json """
        result = False
        try:
            json.dumps(
                self.ufrn_data._request_get(
                    self.ufrn_data.url_package + 'discentes'
                )['resources']
            )
            result = True
        except ValueError as e:
            print(e)
            result = False
        self.assertTrue(result)
