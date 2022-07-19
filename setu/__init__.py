"""Top-level package for Setu UPI DeepLinks SDK."""
from setu.contract import SetuAPIException
from setu.deeplink import Deeplink

__version__ = '2.0.0'

__all__ = ["Deeplink", "SetuAPIException"]
