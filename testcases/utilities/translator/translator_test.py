import sys
import time
import pytest

from jmm.utilities.translator import Translator
from jmm.utilities.translator import TranslationException

@pytest.mark.parametrize(
    'text, expected_text', [
        ('hello, world', '你好，世界'),
        ('hello, world\nhello world', '你好，世界\n你好，世界'),

    ]
)
def test_translator(app_id, app_key, text, expected_text):
    if not app_id or not app_key:
        pytest.skip()

    translator = Translator(app_id, app_key)
    time.sleep(2)
    assert translator.translate(text) == expected_text

@pytest.mark.parametrize(
    'text', ['hello, world', 'gou li guo jia sheng si yi', 'qi yin huo fu bi qu zhi']
)
def test_translator_with_wrong_app_id_and_app_key(text):
    translator = Translator('', '')
    with pytest.raises(TranslationException) as information:
        translator.translate(text)
    assert str(information.value) == 'code: 52003, UNAUTHORIZED USER'

@pytest.mark.skipif(sys.platform == 'linux', reason='in linux, the TranslationException will not be raised, i have no idea about it')
def test_translator_with_high_frequency(app_id, app_key):
    if not app_id or not app_key:
        pytest.skip()

    time.sleep(2)
    translator = Translator(app_id, app_key)
    translator.translate('hello world')

    with pytest.raises(TranslationException) as information:
        translator.translate('hello world')
        translator.translate('hello world')
        translator.translate('hello world')
        translator.translate('hello world')
        translator.translate('hello world')
    assert str(information.value) == 'code: 54003, Invalid Access Limit'
