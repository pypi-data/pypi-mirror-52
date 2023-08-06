"""
Python filesystem tool abstraction layer
"""

from ._config import parse_config
from ._crawler import crawl
from ._structure import restructure

__version__: str = '0.1.6'
