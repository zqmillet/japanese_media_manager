import pathlib

from jmm.utilities.media_finder import MediaFinder

def test_media_finder(directory, file_paths):
    assert len(file_paths) > 0

    media_finder = MediaFinder(directories=[directory], recursively=True, extensions=['.mkv', '.mp4'])

    assert [info.file_path for info in media_finder.get_file_informations()] == list(map(pathlib.Path, ['for_test/star-325.mp4', 'for_test/松本菜奈実/SSNI-306/ssni-306.mkv']))
    assert [info.file_path for info in media_finder.get_file_informations()] == list(map(pathlib.Path, ['for_test/star-325.mp4', 'for_test/松本菜奈実/SSNI-306/ssni-306.mkv']))
    assert not list(media_finder.get_file_informations())[0].has_chinese_subtitle
    assert not list(media_finder.get_file_informations())[1].has_chinese_subtitle
    assert list(media_finder.get_file_informations())[0].number == 'STAR-325'
    assert list(media_finder.get_file_informations())[1].number == 'SSNI-306'

    media_finder = MediaFinder(directories=[directory], recursively=False, extensions=['.mkv', '.mp4'])
    assert [info.file_path for info in media_finder.get_file_informations()] == list(map(pathlib.Path, ['for_test/star-325.mp4']))

    media_finder = MediaFinder(directories=[directory], recursively=False, extensions=['.avi'])
    assert not list(media_finder.get_file_informations())

    media_finder = MediaFinder(directories=[directory], recursively=False, extensions=['.mkv', '.mp4'], minimum_size=1)
    assert not list(media_finder.get_file_informations())

    for file_information in media_finder.get_file_informations():
        print(file_information)
