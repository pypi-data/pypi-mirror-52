"""
Pixiv API library
"""
__version__ = '1.1.7'

from .aapi import AppPixivAPI
from .papi import PixivAPI
from . import error

__all__ = ("PixivAPI", "AppPixivAPI", "error")
