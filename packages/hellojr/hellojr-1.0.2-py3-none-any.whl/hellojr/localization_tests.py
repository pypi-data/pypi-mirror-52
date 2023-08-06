from unittest import TestCase
from click.testing import CliRunner

from .command import cli
from .localization import (
    set_locale,
    get_languages)


class LocalizationTests(TestCase):
    def setUp(self):
        self.runner = CliRunner()

    def test_localization_hello(self):
        """
        Ensure that when the language is switched to french that we see french output.
        """
        set_locale('fr')
        result = self.runner.invoke(cli, ['--hello', 'add', '15', '5'])
        self.assertEquals(result.exit_code, 0)
        self.assertEquals(result.output, 'Bonjour\n15 + 5 = 20\n')

    def test_localization_fallback(self):
        """
        Ensure that using a localized string with an unknown locale returns the original string.
        """
        set_locale('unknown')
        result = self.runner.invoke(cli, ['--hello', 'add', '15', '5'])
        self.assertEquals(result.exit_code, 0)
        self.assertEquals(result.output, 'Hello\n15 + 5 = 20\n')

    def test_localization_get_languages(self):
        """
        Ensure that we can detect the initialized catalogs.
        """
        languages = get_languages()
        print(languages)
        self.assertTrue('en' in languages)
        self.assertTrue('fr' in languages)
