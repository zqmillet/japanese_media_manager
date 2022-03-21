import pathlib

from jmm.utilities.media_finder import MediaFinder

def test_media_finder(directory, file_paths):
    assert len(file_paths) > 0

    media_finder = MediaFinder(directories=[directory], recursively=True, extensions=['.mkv', '.mp4'])

    assert [info.file_path for info in media_finder] == list(map(pathlib.Path, ['for_test/star-325.mp4', 'for_test/松本菜奈実/SSNI-306/ssni-306.mkv']))
    assert [info.file_path for info in media_finder] == list(map(pathlib.Path, ['for_test/star-325.mp4', 'for_test/松本菜奈実/SSNI-306/ssni-306.mkv']))

    media_finder = MediaFinder(directories=[directory], recursively=False, extensions=['.mkv', '.mp4'])
    assert [info.file_path for info in media_finder] == list(map(pathlib.Path, ['for_test/star-325.mp4']))

    media_finder = MediaFinder(directories=[directory], recursively=False, extensions=['.avi'])
    assert not list(media_finder)

    media_finder = MediaFinder(directories=[directory], recursively=False, extensions=['.mkv', '.mp4'], minimum_size=1)
    assert not list(media_finder)
