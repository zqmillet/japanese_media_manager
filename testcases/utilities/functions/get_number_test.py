import pytest

from japanese_media_manager.utilities.functions import get_number

@pytest.mark.parametrize(
    'number, expected_output', [
        ('ipz-111-C', 'IPZ-111'),
        ('mudr-175', 'MUDR-175'),
        ('STARS-071_keyint12', 'STARS-071'),
        ('prtd00002hhb', 'PRTD-002'),
        ('gvg835.HD.mp4', 'GVG-835'),
        ('RBD-501 サイレントレイプ 声を出せない私3 罪深き絶頂に震えて', 'RBD-501'),
        ('RBD-487-CD1', 'RBD-487'),
        ('ipx00052hhb', 'IPX-052'),
        ('ipx00050hhb', 'IPX-050'),
        ('300MIUM-599 【妹にしたい激ウブJD】レンタル彼女で働く可愛い過ぎる10代に猛烈課金→ナマ ちはるちゃん18歳K大学情報学部1年', 'MIUM-599'),
    ]
)
def test_get_number(number, expected_output):
    assert get_number(number) == expected_output
