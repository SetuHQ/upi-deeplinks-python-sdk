"""Top-level package for Setu UPI DeepLinks SDK."""
from setu.contract import SetuAPIException
from setu.deeplink import Deeplink

__version__ = '1.1.1'

__all__ = ["Deeplink", "SetuAPIException"]
