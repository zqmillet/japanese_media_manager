import io
import pytest

from jmm.scripts.generate_configuration import generate_configuration

@pytest.mark.usefixtures('protect_custom_config_file')
def test_generate_configuration(monkeypatch, capsys, custom_config_file_path):
    monkeypatch.setattr('sys.stdin', io.StringIO(''))
    generate_configuration()
    result = capsys.readouterr()
    assert result.out.strip() == f'configuration has been saved in file {custom_config_file_path}'

    monkeypatch.setattr('sys.stdin', io.StringIO('n\n'))
    generate_configuration()
    result = capsys.readouterr()
    assert result.out.strip() == f'file {custom_config_file_path} exists, overwrite it? (Y/n) cancelled by user'

    monkeypatch.setattr('sys.stdin', io.StringIO('yes\nhao\nN'))
    generate_configuration()
    result = capsys.readouterr()
    assert result.out.strip() == f'file {custom_config_file_path} exists, overwrite it? (Y/n) ' * 3 + 'cancelled by user'
