"""module entrypoint for trivial execution"""

from .semtest import semantic_test_runner
from .logcfg import configure_cli_logging

if __name__ == '__main__':
    configure_cli_logging()
    semantic_test_runner()
