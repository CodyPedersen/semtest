"""Entrypoint for the semtest testing framework"""
from .reporting import BenchmarkReport
from .engine import Engine
from .loader import Loader
from .parser import Parser
from .logcfg import configure_cli_logging


def semtest_configure_run() -> None:
    configure_cli_logging()
    semantic_test_runner()

def semantic_test_runner() -> None:
    """Traverse directories and execute relevant semantic tests"""
    context = Parser().parse_arguments()
    loader = Loader(context)
    reporter = BenchmarkReport()
    engine = Engine(
        context=context,
        loader=loader,
        reporter=reporter
    )
    engine.execute()
