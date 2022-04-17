import pathlib

from jmm.utilities.functions import get_file_paths

def test_get_file_paths(directory, file_paths):
    assert len(file_paths) > 0

    _file_paths = get_file_paths(directories=[directory], recursively=True, extensions=['.mkv', '.mp4'])

    assert _file_paths == list(
        map(
            pathlib.Path,
            [
                'for_test/star-325.mp4',
                'for_test/xxx/star-326-cd1.mp4',
                'for_test/xxx/star-326-cd2.mp4',
                'for_test/xxx/star-326-cd3.mp4',
                'for_test/松本菜奈実/SSNI-306/ssni-306.mkv'
            ]
        )
    )

    _file_paths = get_file_paths(directories=[directory], recursively=False, extensions=['.mkv', '.mp4'])
    assert _file_paths == list(map(pathlib.Path, ['for_test/star-325.mp4']))

    assert not get_file_paths(directories=[directory], recursively=False, extensions=['.avi'])
    assert not get_file_paths(directories=[directory], recursively=False, extensions=['.mkv', '.mp4'], minimum_size=1)
