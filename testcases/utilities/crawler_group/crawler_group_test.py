import datetime
import PIL.JpegImagePlugin
import pytest

from jmm.utilities.crawler_group import CrawlerGroup

def test_crawlers_warning(logger, arzon, avsox, javbus):
    CrawlerGroup([arzon], required_fields=['poster', 'stars', 'outline'], logger=logger)
    assert logger == [
        ('info', 'crawlers grouped by <crawler ArzonCrawler> is ready'),
        ('info', '1 field(s): outline can be crawled by this crawler group'),
        ('warning', '2 field(s): poster, stars cannot be crawled by this crawler group')
    ]
    logger.clear()

    CrawlerGroup([avsox, arzon], required_fields=['fanart', 'stars', 'outline'], logger=logger)
    assert logger == [
        ('info', 'crawlers grouped by <crawler AvsoxCrawler>, <crawler ArzonCrawler> is ready'),
        ('info', '3 field(s): fanart, stars, outline can be crawled by this crawler group')
    ]
    logger.clear()

    CrawlerGroup([avsox, arzon, javbus], required_fields=['fanart', 'stars', 'outline', 'poster'], logger=logger)
    assert logger == [
        ('info', 'crawlers grouped by <crawler AvsoxCrawler>, <crawler ArzonCrawler>, <crawler JavBusCrawler> is ready'),
        ('info', '3 field(s): fanart, stars, outline can be crawled by this crawler group'),
        ('warning', '1 field(s): poster cannot be crawled by this crawler group')
    ]
    logger.clear()

@pytest.mark.parametrize(
    'number, metadata, messages', [
        (
            'star-325', {
                'poster': None,
                'keywords': ['STAR-325', 'SODクリエイト', '美人潜入捜査官', 'DVD多士爐', '女檢察官', '潮吹', '偶像藝人', '單體作品', '中出'],
                'title': 'STAR-325 美人潜入捜査官 羽田あい',
                'release_date': datetime.date(2012, 1, 8),
                'runtime': 120,
                'number': 'STAR-325',
                'director': '本田教仁',
                'series': '美人潜入捜査官',
                'studio': 'SODクリエイト',
                'stars': [{'avatar_url': 'https://www.javbus.com/pics/actress/6xv_a.jpg', 'name': '羽田あい'}],
                'outline': '潛入黑暗組織的「羽田亞衣」，雖然登場很瀟灑，不過沒多久就被敵人抓住了！被鎖鍊綁住連續調教，潮吹就像爆炸班狂噴！不斷反覆的凌虐，反而讓她沈溺在當中…。'
            },
            [
                ('info', 'crawlers grouped by <crawler JavBusCrawler>, <crawler JavdbCrawler>, <crawler AirAvCrawler> is ready'),
                ('info', '2 field(s): stars, outline can be crawled by this crawler group'),
                ('warning', '1 field(s): poster cannot be crawled by this crawler group'),
                ('info', 'crawling video star-325 by <crawler JavBusCrawler>'),
                ('info', 'missing 1 field(s): outline'),
                ('info', '<crawler JavdbCrawler> cannot provide more fields, ignore it'),
                ('info', 'crawling video star-325 by <crawler AirAvCrawler>'),
                ('info', 'all fields are crawled'),
            ]
        ),
        (
            'ssni-201', {
                'poster': None,
                'keywords': ['SSNI-201', 'S1NO.1STYLE', '校服', '巨乳', '單體作品', 'DMM獨家', '深喉', '凌辱', '薄馬賽克', '高畫質'],
                'title': 'SSNI-201 全員悪人レ○プ学園 鈴木心春 「もう誰も信じられない…」純粋で真面目な生徒会長は同級生に犯され男性教師に凌辱レ○プされ女性教師にまで折檻責めされて-',
                'release_date': datetime.date(2018, 5, 3),
                'runtime': 140,
                'number':
                'SSNI-201',
                'director': '肉尊',
                'series': None,
                'studio': 'エスワンナンバーワンスタイル',
                'stars': [{'avatar_url': 'https://www.javbus.com/pics/actress/8yw_a.jpg', 'name': '鈴木心春'}],
                'outline': '學生會長鈴木心春發現會計簿中有奇怪的收據，正義感很強的她與男教師談這件事卻遭背叛。這學校裡的教師、同學、朋友都是惡人，沒人願意幫她。讓她在癡漢、剃毛、口爆，凌辱性交中墜落性愛地獄。'
            },
            [
                ('info', 'crawlers grouped by <crawler JavBusCrawler>, <crawler JavdbCrawler>, <crawler AirAvCrawler> is ready'),
                ('info', '2 field(s): stars, outline can be crawled by this crawler group'),
                ('warning', '1 field(s): poster cannot be crawled by this crawler group'),
                ('info', 'crawling video ssni-201 by <crawler JavBusCrawler>'),
                ('info', 'missing 1 field(s): outline'),
                ('info', '<crawler JavdbCrawler> cannot provide more fields, ignore it'),
                ('info', 'crawling video ssni-201 by <crawler AirAvCrawler>'),
                ('info', 'all fields are crawled'),
            ]
        ),
        (
            'hunta-007', {
                'poster': None,
                'keywords': ['HUNTA-007', 'Hunter（ソフトオンデマンド）', '多P', '企畫', '姐妹', '高畫質'],
                'title': 'HUNTA-007 ヘタ過ぎる妹の彼氏に姉の私が直接SEX指導！私の可愛い妹（JK）が初めて家に彼氏を連れて来た。彼氏が真面目そうな子で安心したけど…思春期だし、部屋で2人きりになったらHな事をするに決まっている…。心配',
                'release_date': datetime.date(2015, 5, 21),
                'runtime': 233,
                'number': 'HUNTA-007',
                'director': 'アマゾン円童',
                'series': None,
                'studio': 'Hunter',
                'stars': [
                    {'avatar_url': 'https://www.javbus.com/pics/actress/314_a.jpg', 'name': '南梨央奈'},
                    {'avatar_url': 'https://www.javbus.com/pics/actress/2wr_a.jpg', 'name': '春原未来'},
                    {'avatar_url': 'https://www.javbus.com/pics/actress/944_a.jpg', 'name': '水希杏'},
                    {'avatar_url': 'https://www.javbus.com/pics/actress/895_a.jpg', 'name': '篠宮ゆり'},
                    {'avatar_url': 'https://www.javbus.com/pics/actress/mg9_a.jpg', 'name': '青葉優香'},
                    {'avatar_url': 'https://www.javbus.com/pics/actress/n00_a.jpg', 'name': '白石悠'}
                ],
                'outline': '學生妹首次帶了男友回家來。想說一定在房間幹起來了！但我看了一下發現男友技巧真是超爛！只好進去用肉體來個3P大指導！'
            },
            [
                ('info', 'crawlers grouped by <crawler JavBusCrawler>, <crawler JavdbCrawler>, <crawler AirAvCrawler> is ready'),
                ('info', '2 field(s): stars, outline can be crawled by this crawler group'),
                ('warning', '1 field(s): poster cannot be crawled by this crawler group'),
                ('info', 'crawling video hunta-007 by <crawler JavBusCrawler>'),
                ('info', 'missing 1 field(s): outline'),
                ('info', '<crawler JavdbCrawler> cannot provide more fields, ignore it'),
                ('info', 'crawling video hunta-007 by <crawler AirAvCrawler>'),
                ('info', 'all fields are crawled'),
            ]
        ),
        (
            'rki-460', {
                'poster': None,
                'keywords': ['RKI-460', 'ROOKIE', '中出', '單體作品', 'DMM獨家', '口交', '美少女', '乳房', '女上位', '高畫質'],
                'title': 'RKI-460 世界で一番エロく見える椎名そらの生々しいフェラチオと気持ち良すぎるSEX',
                'release_date': datetime.date(2018, 3, 3),
                'runtime': 130,
                'number': 'RKI-460',
                'director': '真咲南朋',
                'series': None,
                'studio': 'ROOKIE',
                'stars': [{'avatar_url': 'https://www.javbus.com/pics/actress/p84_a.jpg', 'name': '椎名そら'}],
                'outline': '世界で一番エロく見えるライティングとアングルで見せる最高にカワイイ椎名そら！目の前で舐められているかのような臨場感MAXのフェラチオ！ピンク乳首で美乳の天使のおっぱい！プリッとした弾力のあるまん丸のお尻！キュッとしまった美マンコに思いっきり中出し！最高にきれいなフェラチオと最高に気持ちいいSEXでイッちゃう！'
            },
            [
                ('info', 'crawlers grouped by <crawler JavBusCrawler>, <crawler JavdbCrawler>, <crawler AirAvCrawler> is ready'),
                ('info', '2 field(s): stars, outline can be crawled by this crawler group'),
                ('warning', '1 field(s): poster cannot be crawled by this crawler group'),
                ('info', 'crawling video rki-460 by <crawler JavBusCrawler>'),
                ('info', 'missing 1 field(s): outline'),
                ('info', '<crawler JavdbCrawler> cannot provide more fields, ignore it'),
                ('info', 'crawling video rki-460 by <crawler AirAvCrawler>'),
                ('info', 'all fields are crawled'),
            ]
        )
    ]
)
def test_get_metadata(number, metadata, javbus, javdb, airav, logger, messages):
    crawlers = CrawlerGroup([javbus, javdb, airav], required_fields=['poster', 'stars', 'outline'], logger=logger)
    _metadata = crawlers.get_metadata(number)

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
    assert logger == messages

@pytest.mark.parametrize(
    'number, messages, metadata', [
        (
            'FC2-PPV-2608212',
            [
                ('info', 'crawlers grouped by <crawler JavBusCrawler>, <crawler AvsoxCrawler> is ready'),
                ('info', '3 field(s): stars, series, title can be crawled by this crawler group'),
                ('info', 'crawling video FC2-PPV-2608212 by <crawler JavBusCrawler>'),
                ('info', 'missing 3 field(s): series, stars, title'),
                ('info', 'crawling video FC2-PPV-2608212 by <crawler AvsoxCrawler>'),
                ('info', 'missing 1 field(s): stars'),
                ('warning', '1 field(s): stars are not crawled'),
            ],
            {
                'poster': None,
                'keywords': ['素人'],
                'title': 'FC2-PPV-2608212 【個撮】都立チアダンス部② 色白剛毛な清楚美少女\u3000海外留学のために定期的に中出し',
                'release_date': datetime.date(2022, 1, 20),
                'runtime': 9,
                'number': 'FC2-PPV-2608212',
                'director': None,
                'series': '資本主義',
                'studio': 'FC2-PPV',
                'stars': [],
                'outline': None
            }
        ),
        (
            '012222_01',
            [
                ('info', 'crawlers grouped by <crawler JavBusCrawler>, <crawler AvsoxCrawler> is ready'),
                ('info', '3 field(s): stars, series, title can be crawled by this crawler group'),
                ('info', 'crawling video 012222_01 by <crawler JavBusCrawler>'),
                ('info', 'missing 3 field(s): series, stars, title'),
                ('info', 'crawling video 012222_01 by <crawler AvsoxCrawler>'),
                ('info', 'missing 1 field(s): series'),
                ('warning', '1 field(s): series are not crawled'),
            ],
            {
                'poster': None,
                'keywords': ['素人'],
                'title': '012222_01 経験人数がギリ二桁の絶倫娘を紹介してもらいました',
                'release_date': datetime.date(2022, 1, 22),
                'runtime': 55,
                'number': '012222_01',
                'director': None,
                'series': None,
                'studio': '天然むすめ( 10musume )',
                'stars': [{'avatar_url': 'https://us.netcdn.space/storage/heyzo/actorprofile/3000/1211/profile.jpg', 'name': '栗原梢'}],
                'outline': None
            }
        )
    ]
)
def test_get_imcompleted_metadata(number, metadata, messages, avsox, javbus, logger):
    crawlers = CrawlerGroup([javbus, avsox], required_fields=['stars', 'series', 'title'], logger=logger)
    _metadata = crawlers.get_metadata(number)

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
    assert logger == messages
