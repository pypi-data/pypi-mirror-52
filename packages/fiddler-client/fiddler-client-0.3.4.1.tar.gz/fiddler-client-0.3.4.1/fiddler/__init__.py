"""
Fiddler Client Module
=====================

A Python client for Fiddler service.

TODO: Add Licence.
"""

from .fiddler_api import FiddlerApi
from .client import Fiddler
from .client import PredictionEventBundle
from .core_objects import (
    Column,
    DatasetInfo,
    DataType,
    ModelInfo,
    ModelInputType,
    ModelTask,
)

__all__ = [
    'Column',
    'DatasetInfo',
    'DataType',
    'Fiddler',
    'FiddlerApi',
    'ModelInfo',
    'ModelInputType',
    'ModelTask',
    'PredictionEventBundle',
]
