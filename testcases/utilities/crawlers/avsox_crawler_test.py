import datetime
import pytest

from japanese_media_manager.utilities.crawlers import AvsoxCrawler

@pytest.mark.parametrize(
    'number, release_date, length, studio, title, keywords, stars, series', [
        (
            'Jukujo2474',
            '2022-02-05',
            59,
            '熟女倶楽部( Jukujo Club )',
            'Jukujo2474 有田典子\u3000旦那とAV出演編',
            ['素人'],
            [{'avatar_url': 'https://jp.netcdn.space/mono/actjpgs/nowprinting.gif', 'name': '有田典子'}],
            '三十路',
        ),
        (
            'FC2-PPV-2645773',
            '2022-02-05',
            36,
            'FC2-PPV',
            'FC2-PPV-2645773 初撮影【新シネマ画風】個数限定【無修正】どこか寂しげで一途で真面目な女子大生・・・徐々に色濃く乱れていく美白の身体に2回膣内射精。恋に落ちいる寒い日の夜だった（長編）',
            ['素人'],
            [],
            'ネオペイ',
        ),
        (
            'HEYZO-2713',
            '2022-02-06',
            60,
            'HEYZO',
            'HEYZO-2713 安芸美咲 【あきみさき】 欲求不満なヤリたがりセフレをハメ倒してヤッた',
            ['内射'],
            [{'avatar_url': 'https://us.netcdn.space/storage/heyzo/actorprofile/3000/1215/profile.jpg', 'name': '安芸美咲'}],
            None,
        ),
        (
            'FC2-PPV-2639303',
            '2022-02-05',
            62,
            'FC2-PPV',
            'FC2-PPV-2639303 独占販売第34貝 さや 20代 千葉県在住 職業非公開 正統派清楚系スレンダー美女 敏感な陥没乳首 クンニやおもちゃで細い身体をのけ反らせて絶頂 最後は引き締まった腹筋に濃い精子をぶっかけ大量射精',
            ['素人'],
            [],
            'クリストフ・ハメール',
        ),
        (
            '020322_001',
            '2022-02-03',
            61,
            '一本道( 1pondo )',
            '020322_001 モデルコレクション 森田みゆ',
            ['苗条'],
            [{'avatar_url': 'https://us.netcdn.space/storage/heyzo/actorprofile/3000/1096/profile.jpg', 'name': '森田みゆ'}],
            'モデルコレクション',
        ),
        (
            '012222_01',
            '2022-01-22',
            55,
            '天然むすめ( 10musume )',
            '012222_01 経験人数がギリ二桁の絶倫娘を紹介してもらいました',
            ['素人'],
            [{'avatar_url': 'https://us.netcdn.space/storage/heyzo/actorprofile/3000/1211/profile.jpg', 'name': '栗原梢'}],
            None,
        ),
        (
            'FC2-PPV-2608212',
            '2022-01-20',
            9,
            'FC2-PPV',
            'FC2-PPV-2608212 【個撮】都立チアダンス部② 色白剛毛な清楚美少女　海外留学のために定期的に中出し',
            ['素人'],
            [],
            '資本主義',
        ),
    ]
)
def test_avsox_metadata(number, release_date, length, studio, title, keywords, stars, series, proxies):
    crawler = AvsoxCrawler(proxies=proxies, verify=False)
    metadata = crawler.get_metadata(number)

    assert metadata['number'] == number
    assert metadata['release_date'] == datetime.datetime.strptime(release_date, '%Y-%m-%d').date()
    assert metadata['length'] == length
    assert metadata['studio'] == studio
    assert metadata['title'] == title
    assert metadata['keywords'] == keywords
    assert metadata['stars'] == stars
    assert metadata['series'] == series
    assert metadata['fanart'] is not None
    assert metadata['poster'] is None

@pytest.mark.parametrize('number', ['XXX-1234', 'yyy-2333', 'gouliguojiashengsiyi'])
def test_avsox_metadata_with_nonexistent_number(number, proxies):
    crawler = AvsoxCrawler(proxies=proxies, verify=False)
    metadata = crawler.get_metadata(number)

    assert metadata['number'] == number
    assert metadata['release_date'] is None
    assert metadata['length'] is None
    assert metadata['studio'] is None
    assert metadata['title'] is None
    assert metadata['series'] is None
    assert metadata['fanart'] is None
    assert metadata['poster'] is None
    assert not metadata['keywords']
    assert not metadata['stars']
