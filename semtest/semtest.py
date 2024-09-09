"""Entrypoint for the semtest testing framework"""
from .parser import Parser

def semantic_test_runner() -> None:
    """Traverse directories and execute relevant semantic tests"""

    parser = Parser()
    res = parser.parse_arguments()
    _ = res
