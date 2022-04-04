from pathlib import Path

from jmm.utilities.file_information import FileInformation

def test_get_file_paths(file_paths):
    file_informations = list(map(FileInformation, map(Path, file_paths)))

    assert not file_informations[0].has_chinese_subtitle
    assert not file_informations[1].has_chinese_subtitle
    assert file_informations[0].number == 'STAR-325'
    assert file_informations[1].number == 'SSNI-306'
