import yaml
import pytest

from jmm.scripts.valid_configuration import valid_configuration
from jmm.scripts.constants import custom_configuration_path

@pytest.fixture(name='write_configuration', scope='function')
def _write_configuration(proxies, directory):
    configuration = {
        'crawlers': [
            {
                'name': 'javbus',
                'class': 'jmm.crawlers.JavBusCrawler',
                'with': {'proxies': proxies.dict()}
            },
            {
                'name': 'javbooks',
                'class': 'jmm.crawlers.JavBooksCrawler',
                'with': {'proxies': proxies.dict()}
            }
        ],
        'routing_rules': [
            {
                'pattern': r'\w+-\d+',
                'crawler_names': ['javbooks', 'javbus']
            }
        ],
        'media_finder': {
            'extensions': ['avi', 'mp4'],
            'recursive': True,
            'minimum_size': 1025,
            'directories': [directory]
        }
    }

    with open(custom_configuration_path, 'w', encoding='utf8') as file:
        file.write(yaml.safe_dump(configuration))

@pytest.mark.usefixtures('write_configuration')
@pytest.mark.usefixtures('protect_custom_config_file')
def test_test_configuration(capsys):
    valid_configuration(['star-325', 'ssis-334', 'atid-233'])
    output, _ = capsys.readouterr()

    assert 'あいださく' in output
    assert '神波多一花' in output
    assert '家庭教師と生徒の秘め事' in output

@pytest.mark.usefixtures('write_configuration')
@pytest.mark.usefixtures('protect_custom_config_file')
def test_test_configuration_with_invalid_number():
    with pytest.raises(Exception) as information:
        valid_configuration(['gouliguojiashengsiyi', 'qiyinhuofubiquzhi'])

    assert str(information.value) == "there is no routing rule matches this type of number 'gouliguojiashengsiyi'"
