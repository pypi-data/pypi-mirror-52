from unittest import TestCase
from click.testing import CliRunner

from .command import cli


class CommandTests(TestCase):
    def setUp(self):
        self.runner = CliRunner()

    def test_add_command_valid_arguments(self):
        """
        Ensure that valid integers can be be added via the add command.
        """
        result = self.runner.invoke(cli, ['add', '5', '5'])
        self.assertEquals(result.exit_code, 0)
        self.assertEquals(result.output, '5 + 5 = 10\n')

    def test_add_command_invalid_arguments(self):
        """
        Ensure that invalid integers cannot be added.
        """
        result = self.runner.invoke(cli, ['add', '5', 'b'])
        self.assertEquals(result.exit_code, 2)
        self.assertTrue('Invalid value for "b": b is not a valid integer\n' in result.output)

    def test_hello_option(self):
        """
        Ensure that the --hello option works as expected.
        """
        result = self.runner.invoke(cli, ['--hello', 'add', '15', '5'])
        self.assertEquals(result.exit_code, 0)
        self.assertEquals(result.output, 'Hello\n15 + 5 = 20\n')

    def test_multiply_command_valid_arguments(self):
        """
        Ensure that valid integers can be be multiplied via the multiply command.
        """
        result = self.runner.invoke(cli, ['multiply', '5', '5'])
        self.assertEquals(result.exit_code, 0)
        self.assertEquals(result.output, '5 * 5 = 25\n')

    def test_multiply_command_invalid_arguments(self):
        """
        Ensure that invalid integers cannot be multiplied.
        """
        result = self.runner.invoke(cli, ['multiply', '5', 'b'])
        self.assertEquals(result.exit_code, 2)
        self.assertTrue('Invalid value for "b": b is not a valid integer\n' in result.output)

    def test_unknown_command(self):
        """
        Ensure that unknown commands trigger an error.
        """
        result = self.runner.invoke(cli, ['subtract', '5', '5'])
        self.assertEquals(result.exit_code, 2)
        self.assertTrue('Error: No such command "subtract".\n' in result.output)
