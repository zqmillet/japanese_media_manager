"""
由于很多网站都是日语的元数据, 因此需要翻译模块对元数据进行翻译.
"""

from .translator import Translator
from .exceptions import TranslationException

__all__ = ['Translator', 'TranslationException']
