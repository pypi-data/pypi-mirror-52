from .utils import *


class Package(unittest.TestCase):
    def setUp(self):
        """Inicia novo objeto em todo os testes."""
        self.ufrn_data = ODUFRNDownloader()

    def test_can_print_packages(self):
        """Verifica se a lista de packages é impressa na tela."""
        assert_console(self.ufrn_data.print_packages)

    def test_can_load_packages(self):
        """Verifica se a lista de packages é carregada no objeto."""
        self.ufrn_data.load_packages()
        self.assertTrue(len(self.ufrn_data.available_packages) > 0)

    def test_search_packages(self):
        """Verifica se a procura por pacotes está funcionando."""
        list_groups = self.ufrn_data.search_related_packages('discent')
        self.assertTrue(len(list_groups) == 3)
        list_groups = self.ufrn_data.search_related_packages('disc', True)
        self.assertTrue(len(list_groups) == 3)
        list_groups = self.ufrn_data.search_related_packages('disc')
        self.assertTrue(len(list_groups) == 0)

    def test_can_download_package(self):
        """Verifica se baixa-se arquivos de um grupo"""
        self.ufrn_data.download_package('telefones', './tmp')
        self.assertTrue(os.path.exists('./tmp/telefones'))
        if os.path.exists('./tmp'):
            shutil.rmtree('./tmp')

    def test_can_download_packages(self):
        """Verifica se baixa-se arquivos de um pacote"""
        self.ufrn_data.download_packages(
            ['telefones', 'unidades-academicas'], './tmp'
        )
        telefone_path = os.path.exists('./tmp/telefones')
        unidades_path = os.path.exists('./tmp/unidades-academicas')
        self.assertTrue(telefone_path and unidades_path)
        if os.path.exists('./tmp'):
            shutil.rmtree('./tmp')

    def test_can_print_files_from_package(self):
        """Verifica se os arquivos de um pacote podem ser impressos na tela."""
        assert_console(
            lambda: self.ufrn_data.print_files_from_package('discentes')
        )

    def test_can_print_files_from_package_with_typo(self):
        """Verifica se o tratamento de erro com o Levenshtein funciona."""
        assert_console(
            lambda: self.ufrn_data.print_files_from_package('discente')
        )

    def test_can_print_not_relation(self):
        """Verifica se imprime não haver relação de pacote."""
        self.ufrn_data.warnings = True
        assert_console(
            lambda: self.ufrn_data.search_related_packages(
                'asudsada', True, True
            )
        )

    def test_can_download_packages_filtering_years(self):
        """Verifica se baixa-se pacote filtrando por anos"""
        self.ufrn_data.download_package('discentes', './tmp', years=[2018])
        _, _, files = next(os.walk('./tmp/discentes'))
        file_exist = os.path.exists('./tmp/discentes/Ingressantes em 2018.csv')
        self.assertTrue(len(files) > 0 and file_exist)
        if os.path.exists('./tmp'):
            shutil.rmtree('./tmp')
