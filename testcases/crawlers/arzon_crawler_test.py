import datetime
import pytest

from jmm.crawlers import ArzonCrawler

@pytest.mark.parametrize(
    'number, metadata', [
        (
            'STAR-325',
            {
                'title': '美人潜入捜査官 羽田あい',
                'outline': '黒のラバースーツを身に纏い、闇の組織と立ち向かう潜入捜査官・あいが敵に捕らわれてしまった！鎖で繋がれた連続イカセで潮が爆噴射状態！脈打つ塊を淫汁であふれるマ○コにぶち込まれ大量の連続中出し！',
                'series': 'ＳＯＤｓｔａｒ',
                'studio': 'ＳＯＤクリエイト（ソフトオンデマンド）',
                'director': '本田教仁',
                'runtime': 120,
                'number': 'STAR-325',
                'release_date': datetime.date(2011, 12, 8)
            }
        ),
        (
            'ATKD-246',
            {
                'director': '',
                'runtime': 480,
                'number': 'ATKD-246',
                'outline': '恥ずかしい尻穴を徹底的に犯され尽くす！日を追うごとに快楽に飲み込まれ、悦楽にひれ伏す哀しき女たち…。凌辱ドラマの殿堂アタッカーズがお届するアナルシーンのみ厳選した16タイトル8時間！被虐の肛門性交！',
                'release_date': datetime.date(2016, 11, 19),
                'series': 'ATTACKERS',
                'studio': 'アタッカーズ',
                'title': 'ATTACKERS 凌辱アナル480分総集編3'
            },
        ),
        (
            'WANZ-211',
            {
                'director': '',
                'runtime': 120,
                'number': 'WANZ-211',
                'outline': 'お嬢様は、潜入捜査官。モデル顔負けの８頭身！女を薬漬けにし、人身売買をしている悪徳プロダクションへ潜入。'
                'しかしその美しさは、所属しているアイドルの嫉妬をかってしまう。薬を盛られ下衆に犯される！正義を逆手に取られ屈辱のおしゃぶり喉奥射精！'
                'スーパーボディの高級マンコが便所で拘束開放！そして恐怖のオマンコ握手会が開催される！嫉妬ブスからナジられ、タダ同然でオタク共に膣内射精される地獄が始まる',
                'release_date': datetime.date(2014, 7, 1),
                'series': 'WANZ',
                'studio': 'ワンズファクトリー',
                'title': '美人潜入捜査官 神波多一花'
            }
        )
    ]
)
def test_arzon_metadata(number, metadata, proxies):
    crawler = ArzonCrawler(proxies=proxies)
    _metadata = crawler.get_metadata(number)

    assert {
        'title': _metadata.title,
        'number': _metadata.number,
        'outline': _metadata.outline,
        'series': _metadata.series,
        'studio': _metadata.studio,
        'director': _metadata.director,
        'runtime': _metadata.runtime,
        'release_date': _metadata.release_date,
    } == metadata

@pytest.mark.parametrize('number', ['XXX-250', 'SB-250'])
def test_arzon_metadata_with_nonexistent_number(number, proxies):
    crawler = ArzonCrawler(proxies=proxies)
    metadata = crawler.get_metadata(number)

    assert metadata.fanart is None
    assert metadata.poster is None
    assert metadata.title is None
    assert metadata.number == number
    assert metadata.outline is None
    assert metadata.series is None
    assert metadata.studio is None
    assert metadata.director is None
    assert metadata.runtime is None
    assert metadata.release_date is None
    assert not metadata.stars
