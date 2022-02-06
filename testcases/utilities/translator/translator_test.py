import time
import pytest

from japanese_media_manager.utilities.translator import Translator

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
