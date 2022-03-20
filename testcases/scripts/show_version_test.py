from jmm import  VERSION

from jmm.scripts.show_version import show_version

def test_show_version(capsys):
    show_version()
    output, _ = capsys.readouterr()
    assert output.strip() == VERSION
