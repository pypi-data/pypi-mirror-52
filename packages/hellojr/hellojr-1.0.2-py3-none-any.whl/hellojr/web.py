"""
HTTP views for flask that allow adding and multiplying integers together.
"""

from flask import Flask

from .addition import add
from .multiplication import multiply


app = Flask(__name__)


@app.route('/add/<int:a>/<int:b>')
def add_view(a: int, b: int) -> str:
    """
    HTTP view that returns the result of adding two integers together.
    """
    return str(add(a, b))


@app.route('/multiply/<int:a>/<int:b>')
def multiply_view(a: int, b: int) -> str:
    """
    HTTP view that returns the result of multiplying two integers together.
    """
    return str(multiply(a, b))
