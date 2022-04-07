import pytest

from jmm.utilities.translator import Translator
from jmm.utilities.file_manager import FileManager
from jmm.utilities.file_manager import Mode

@pytest.fixture(name='translator', scope='function')
def _translator(app_id, app_key):
    return Translator(app_id, app_key)

@pytest.mark.parametrize(
    'text, expected_output', [
        ('', ''),
        (None, ''),
        ('gouliguojiashengsiyi', 'gouliguojiashengsiyi')
    ]
)
def test_file_manager_translate(text, expected_output):
    file_manager = FileManager(file_path_pattern='{number}{suffix}', mode=Mode.LINK)
    assert file_manager.translate(text) == expected_output

@pytest.mark.parametrize(
    'text, expected_output', [
        ('', ''),
        (None, ''),
        ('gouliguojiashengsiyi', 'gouliguojiashengsiyi')
    ]
)
def test_file_manager_translate_with_translator(text, expected_output, translator):
    file_manager = FileManager(file_path_pattern='{number}{suffix}', mode=Mode.LINK, translator=translator)
    assert file_manager.translate(text) == expected_output
