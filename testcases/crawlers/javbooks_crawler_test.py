import datetime
import PIL
import pytest

from jmm.crawlers import JavBooksCrawler

@pytest.mark.parametrize(
    'number, metadata', [
        (
            'star-325',
            {
                'poster': None,
                'keywords': ['潮吹', '偶像艺人', '中出', '女检察官', '单体作品'],
                'title': '美人潜入捜査官 羽田あい',
                'release_date': datetime.date(2012, 1, 8),
                'runtime': 120,
                'number': 'STAR-325',
                'director': '本田教仁',
                'series': '美人潜入捜査官',
                'studio': 'SODクリエイト',
                'stars': [{'avatar_url': 'https://pics.dmm.co.jp/mono/actjpgs/haneda_ai.jpg', 'name': '羽田あい'}],
                'outline': None
            }
        ),
        (
            'SSNI-385',
            {
                'poster': None,
                'keywords': ['薄马赛克', '单体作品', '美少女', 'デカチン・巨根', '潮吹', '花痴', 'DMM独家', '高画质', 'キス・接吻'],
                'title': '絶頂ポルチオ開発 巨根×膣中イキオーガズム 坂道みる',
                'release_date': datetime.date(2018, 12, 29),
                'runtime': 180,
                'number': 'SSNI-385',
                'director': 'X',
                'series': '絶頂ポルチオ開発 巨根×膣中イキオーガズム',
                'studio': 'エスワン ナンバーワンスタイル',
                'stars': [{'avatar_url': 'https://pics.dmm.co.jp/mono/actjpgs/sakamiti_miru.jpg', 'name': '坂道みる'}],
                'outline': None
            }
        ),
        (
            'SSNI-344',
            {
                'poster': None,
                'keywords': ['高画质', '单体作品', '新娘、年轻妻子', '巨乳', 'DMM独家', '薄马赛克', '偶像艺人'],
                'title': '義父に初めて犯されたあの日から… 三上悠亜',
                'release_date': datetime.date(2018, 11, 17),
                'runtime': 149,
                'number': 'SSNI-344',
                'director': '紋℃',
                'series': '高画质',
                'studio': 'エスワン ナンバーワンスタイル',
                'stars': [{'avatar_url': 'https://pics.dmm.co.jp/mono/actjpgs/mikami_yua.jpg', 'name': '三上悠亜'}],
                'outline': None
            }
        ),
        (
            'AUKG-535',
            {
                'poster': None,
                'keywords': ['故事集', '女同性恋', '恋腿癖', '姐姐', '0', 'DMM独家', '高画质'],
                'title': 'ノーパンパンストレズビアン ～匂うつま先、テカる美脚のパンストマニアックス～',
                'release_date': datetime.date(2022, 2, 26),
                'runtime': 117,
                'number': 'AUKG-535',
                'director': 'U＆K',
                'series': '故事集',
                'studio': 'U＆K',
                'stars': [
                    {'avatar_url': 'https://pics.dmm.co.jp/mono/actjpgs/takeuti_natuki.jpg', 'name': '竹内夏希'},
                    {'avatar_url': 'https://pics.dmm.co.jp/mono/actjpgs/nowprinting.gif', 'name': '木村穂乃香'},
                    {'avatar_url': 'https://pics.dmm.co.jp/mono/actjpgs/toono_miho.jpg', 'name': '通野未帆'},
                    {'avatar_url': 'https://pics.dmm.co.jp/mono/actjpgs/kawana_ai2.jpg', 'name': '河奈亜依'},
                    {'avatar_url': 'https://pics.dmm.co.jp/mono/actjpgs/mutou_ayaka.jpg', 'name': '武藤あやか'},
                    {'avatar_url': 'https://pics.dmm.co.jp/mono/actjpgs/nowprinting.gif', 'name': '市来まひろ'}
                ],
                'outline': None}
        ),
    ]
)
def test_javbooks_crawler_test(proxies, number, metadata):
    crawler = JavBooksCrawler(proxies=proxies)
    _metadata = crawler.get_metadata(number)
    assert isinstance(_metadata.fanart, PIL.JpegImagePlugin.JpegImageFile)
    assert {
        'poster': _metadata.poster,
        'keywords': _metadata.keywords,
        'title': _metadata.title,
        'release_date': _metadata.release_date,
        'runtime': _metadata.runtime,
        'number': _metadata.number,
        'director': _metadata.director,
        'series': _metadata.series,
        'studio': _metadata.studio,
        'stars': [{'avatar_url': star.avatar_url, 'name': star.name} for star in _metadata.stars],
        'outline': _metadata.outline
    } == metadata
    for star in _metadata.stars:
        print(star)
    print(_metadata)

@pytest.mark.parametrize('number', ['SB-250', 'gouliguojiashengsiyi'])
def test_nonexistent_number(proxies, number):
    crawler = JavBooksCrawler(proxies=proxies)
    metadata = crawler.get_metadata(number)

    assert not metadata.keywords
    assert not metadata.stars
    assert metadata.title is None
    assert metadata.release_date is None
    assert metadata.runtime is None
    assert metadata.number == number
    assert metadata.director is None
    assert metadata.series is None
    assert metadata.studio is None
    assert metadata.fanart is None
    assert metadata.poster is None
    assert metadata.outline is None
    print(metadata)
