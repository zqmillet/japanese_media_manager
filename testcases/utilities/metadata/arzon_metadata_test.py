import datetime
import pytest

from japanese_media_manager.utilities.metadata import ArzonMetaData

@pytest.mark.parametrize(
    'number, title, outline, stars, series, studio, director, length, release_date', [
        (
            'STAR-325',
            '美人潜入捜査官 羽田あい',
            '黒のラバースーツを身に纏い、闇の組織と立ち向かう潜入捜査官・あいが敵に捕らわれてしまった！鎖で繋がれた連続イカセで潮が爆噴射状態！脈打つ塊を淫汁であふれるマ○コにぶち込まれ大量の連続中出し！',
            [{'name': '羽田あい', 'avatar_url': 'https://img.arzon.jp/image/3/50/50788S.jpg'}],
            'ＳＯＤｓｔａｒ',
            'ＳＯＤクリエイト（ソフトオンデマンド）',
            '本田教仁',
            ('120', '分'),
            '2011-12-08'
        )
    ]
)
def test_arzon_metadata(number, title, outline, stars, series, studio, director, length, release_date, proxies):
    metadata = ArzonMetaData(number, proxies=proxies)

    assert metadata.fanart is None
    assert metadata.title == title
    assert metadata.number == number
    assert metadata.outline == outline
    assert metadata.stars == stars
    assert metadata.series == series
    assert metadata.studio == studio
    assert metadata.director == director
    assert metadata.length == length
    assert metadata.release_date == datetime.datetime.strptime(release_date, '%Y-%m-%d').date()
