import pytest

from japanese_media_manager.utilities.get_number import get_number

@pytest.mark.parametrize(
    'number, expected_output', [
        ('star-325', 'STAR-325'),
        ('star325', 'STAR-325'),
        ('STAR325', 'STAR-325'),
        ('STAR 325', 'STAR-325'),
        ('star 325', 'STAR-325'),
        ('star-325-c', 'STAR-325'),
        ('star-325-C', 'STAR-325'),
        ('star-325-CD1', 'STAR-325'),
        ('star-325-CD2', 'STAR-325'),
        ('star_325-CD2', 'STAR-325'),
        ('star_325.CD2', 'STAR-325'),
        ('100221_001', '100221_001'),
        ('100221_001', '100221_001'),
        ('100221_001.mkv', '100221_001'),
        ('100221_001hdd.mkv', '100221_001'),
        ('100221_001-C.mkv', '100221_001'),
    ]
)
def test_get_number(number, expected_output):
    assert get_number(number) == expected_output
