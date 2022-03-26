import datetime
import sys
import pytest

from jmm.crawlers import JavdbCrawler

@pytest.mark.skipif(sys.platform != 'darwin', reason='this testcase is passed only in macos')
@pytest.mark.parametrize(
    'number, keywords, title, release_date, runtime, director, series, studio, stars', [
        (
            'star-325',
            ['中出', '單體作品', '潮吹', '藝人', '女檢察官'],
            'STAR-325 美人潜入捜査官 羽田あい',
            '2011-12-08',
            120,
            '本田教仁',
            '美人潜入捜査官',
            'SOD Create',
            [
                {'name': '羽田あい', 'avatar_url': 'https://jdbimgs.com/avatars/rx/rxbJ.jpg'},
                {'name': '佐川銀次', 'avatar_url': 'https://jdbimgs.com/avatars/6j/6JRE.jpg'},
                {'name': 'トニー大木', 'avatar_url': 'https://jdbimgs.com/avatars/yp/YPKz.jpg'}
            ]
        ),
        (
            'ipx-052',
            ['單體作品', '美少女', '調教', '潮吹', '捆綁', '數位馬賽克'],
            'IPX-052 緊縛調教を懇願 イキ狂う変態マゾ幼妻 緊縛解禁！！深く喰い込む麻縄の苦痛と快感に犯され歓喜の絶頂… 桃乃木かな',
            '2017-12-01',
            120,
            None,
            '緊縛マゾ女',
            'IDEA POCKET',
            [
                {'name': '桃乃木香奈, 桃乃木かな', 'avatar_url': 'https://jdbimgs.com/avatars/0d/0dKX.jpg'},
                {'name': '沢木和也', 'avatar_url': 'https://jdbimgs.com/avatars/ak/ak4Or.jpg'},
                {'name': '小田切ジュン', 'avatar_url': 'https://jdbimgs.com/avatars/g9/G955.jpg'}
            ]
        ),
        (
            'ssni-011',
            ['單體作品', '羞恥', '美少女', '凌辱', '輪姦', '薄馬賽克'],
            'SSNI-011 ヲタサーの姫 キモオタ輪姦映像 地下アイドル活動をしていたわたしは、貢いで貰う為に‘オタサーの姫’をしていた事がバレて…汗臭い囲い（キモオタ）に汁まみれにされました。 小島みなみ',
            '2017-09-29',
            120,
            'X',
            'ヲタサーの姫',
            'S1 NO.1 STYLE',
            [
                {'name': '小島南, 小島みなみ', 'avatar_url': 'https://jdbimgs.com/avatars/a2/A2Q0.jpg'},
                {'name': '今井勇太', 'avatar_url': 'https://jdbimgs.com/avatars/1b/1BeOY.jpg'}
            ]
        ),
        (
            'STARS-071',
            ['肌肉', '單體作品', '戲劇', '偶像'],
            'STARS-071 アイドルハンターにピンサロバイトをネタに脅され輪姦されても心だけは屈しなかったアイドル 七海ティナ',
            '2019-05-09',
            110,
            '鎗ヶ崎一',
            None,
            'SOD Create',
            [
                {'name': '七海蒂娜, 七海ティナ', 'avatar_url': 'https://jdbimgs.com/avatars/gb/gbbZ.jpg'},
                {'name': '藍井優太', 'avatar_url': 'https://jdbimgs.com/avatars/dd/Ddd8.jpg'},
                {'name': '井口', 'avatar_url': 'https://jdbimgs.com/avatars/p3/p3NEk.jpg'},
                {'name': '向理来', 'avatar_url': 'https://jdbimgs.com/avatars/eg/egPR.jpg'},
                {'name': '今井勇太', 'avatar_url': 'https://jdbimgs.com/avatars/1b/1BeOY.jpg'}
            ]
        ),
        (
            'MIDE-876',
            ['美乳', '女教師', '濫交', '單體作品', '口交'],
            'MIDE-876 女教師レ×プ輪●～鬼畜イラマ・集団汚辱～ 八木奈々',
            '2021-02-01',
            150,
            '前田文豪',
            '女教師 レイプ 輪姦',
            'MOODYZ',
            [
                {'name': '八木奈々', 'avatar_url': 'https://jdbimgs.com/avatars/ge/gEkm.jpg'},
                {'name': '吉野篤史', 'avatar_url': 'https://jdbimgs.com/avatars/2a/2aV7m.jpg'}
            ]
        )
    ]
)
def test_javdb_metadata(number, keywords, title, release_date, runtime, director, series, studio, stars):
    crawler = JavdbCrawler()
    metadata = crawler.get_metadata(number)

    assert metadata.title == title
    assert metadata.keywords == keywords
    assert metadata.release_date == datetime.datetime.strptime(release_date, '%Y-%m-%d').date()
    assert metadata.runtime == runtime
    assert metadata.number == number.upper()
    assert metadata.director == director
    assert metadata.series == series
    assert metadata.studio == studio
    assert metadata.fanart is not None
    assert metadata.poster is None
    assert metadata.outline is None
    assert [{'name': star.name, 'avatar_url': star.avatar_url} for star in metadata.stars] == stars
    for star in metadata.stars:
        print(star)
    print(metadata)

@pytest.mark.skipif(sys.platform != 'darwin', reason='this testcase is passed only in macos')
@pytest.mark.parametrize('number', ['SB-250', 'gouliguojiashengsiyi'])
def test_metadata_with_nonexistent_number(number):
    crawler = JavdbCrawler()
    metadata = crawler.get_metadata(number)

    assert not metadata.keywords
    assert not metadata.stars
    assert metadata.title is None
    assert metadata.release_date is None
    assert metadata.director is None
    assert metadata.runtime is None
    assert metadata.number == number
    assert metadata.series is None
    assert metadata.studio is None
    assert metadata.fanart is None
    assert metadata.poster is None
    assert metadata.outline is None
    print(metadata)
