"""
Command line tool for the hellojr package
"""

import click

from .addition import add
from .multiplication import multiply

from .localization import _


@click.group()
@click.option('--hello/--no-hello', default=False)
def cli(hello):
    """
    A simple command line tool demonstration.
    """
    if hello:
        # Display a translated message
        click.echo(_('Hello'))


@cli.command('add')
@click.argument('a', type=click.INT)
@click.argument('b', type=click.INT)
def add_command(a: int, b: int):
    """
    Add two integers together and display the result.
    """
    print(f'{a} + {b} = {add(a, b)}')


@cli.command('multiply')
@click.argument('a', type=click.INT)
@click.argument('b', type=click.INT)
def multiply_command(a: int, b: int):
    """
    Multiply two integers together and display the result.
    """
    print(f'{a} * {b} = {multiply(a, b)}')
