"""Entrypoint for the semtest testing framework"""
from .config import configure_cli_logging
from .reporting import BenchmarkReport
from .engine import Engine
from .loader import Loader
from .parser import Parser

def semantic_test_runner() -> None:
    """Traverse directories and execute relevant semantic tests"""

    configure_cli_logging()

    parser = Parser()
    context = parser.parse_arguments()
    loader = Loader(context)
    reporter = BenchmarkReport()
    engine = Engine(
        context=context,
        loader=loader,
        reporter=reporter
    )
    engine.execute()
