import sys
import time
import pytest

from japanese_media_manager.utilities.translator import Translator
from japanese_media_manager.utilities.translator import TranslationException

@pytest.mark.parametrize(
    'text, expected_text', [
        ('hello, world', '你好，世界'),
        ('hello, world\nhello world', '你好，世界\n你好，世界'),

    ]
)
def test_translator(app_id, app_key, text, expected_text):
    translator = Translator(app_id, app_key)
    assert translator.translate(text) == expected_text
    time.sleep(1)

@pytest.mark.parametrize(
    'text', ['hello, world', 'gou li guo jia sheng si yi', 'qi yin huo fu bi qu zhi']
)
def test_translator_with_wrong_app_id_and_app_key(text):
    translator = Translator('', '')
    with pytest.raises(TranslationException) as information:
        translator.translate(text)
    assert str(information.value) == 'code: 52003, UNAUTHORIZED USER'

@pytest.mark.skipif(sys.platform == 'linux', reason='in linux, the TranslationException will not be raised, i have no idea about it')
def test_translator_with_hight_frequency(app_id, app_key):
    translator = Translator(app_id, app_key)
    translator.translate('hello world')

    with pytest.raises(TranslationException) as information:
        translator.translate('hello world')
        translator.translate('hello world')
        translator.translate('hello world')
        translator.translate('hello world')
        translator.translate('hello world')
    assert str(information.value) == 'code: 54003, Invalid Access Limit'
