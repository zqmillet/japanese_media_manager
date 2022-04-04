import datetime
import pytest

from jmm.crawlers import AirAvCrawler

@pytest.mark.parametrize(
    'number, title, outline, keywords, studio, release_date', [
        (
            'SSNI-412',
            '軽蔑目光驚慌失措露內褲 夢乃愛華',
            '被清純的女孩子嫌棄著給你看內褲的激情興奮180分鐘。一遍特地卷起長裙一遍輕蔑的給你看內褲，陪酒女孩的閉嘴輕蔑露內褲做愛！神女的替身謝罪輕蔑露內褲乳交！學生的強求輕蔑露內褲做愛！女僕的嘲諷輕蔑露內褲口交！妹妹的懇願露內褲做愛！真是沒有辦法的變態呢！',
            [],
            None,
            None,
        ),
        (
            'STAR-325',
            '美女潛入搜查官 羽田亞衣',
            '潛入黑暗組織的「羽田亞衣」，雖然登場很瀟灑，不過沒多久就被敵人抓住了！被鎖鍊綁住連續調教，潮吹就像爆炸班狂噴！不斷反覆的凌虐，反而讓她沈溺在當中…。',
            ['潮吹', '中出', '中文字幕', 'AV女優片', '藝人', '女搜查官'],
            'SOD',
            datetime.date(2011, 12, 8),
        ),
        (
            'ABP-888',
            '傳說的超高級沙龍 究極M性感 秘密倶樂部 讓乙都咲乃玩弄個夠！！',
            '蚊香射專屬女優女優『乙都咲乃』今天要讓您覺醒M心…。都內某處寂靜的店裡，只有熟客才知道的完全會員制高級M性感『秘密俱樂部』。高等級S孃的玩弄技巧，讓全國的紳士們都聚集起來。人氣的女王乙都咲乃，玩弄著肉棒展現恍惚微笑，給予M男們至極的褒獎…',
            ['顏射', 'AV女優片', '玩具', 'M男', 'HD高畫質', '男の潮吹き'],
            'PRESTIGE',
            datetime.date(2019, 8, 16),
        ),
        (
            'ABP-960',
            '包下溫泉和美少女肏翻天 08 涼森玲夢',
            '這次和蚊香社女優涼森玲夢包下溫泉去泡湯、一到露天溫泉就忍不住開始愛撫起來、彼此激情肏到爽翻天、快來享受一下這兩天一夜的幹砲泡湯旅吧！',
            ['SM', '巨乳', '拘束', '乳交', 'AV女優片', '玩具'],
            'PRESTIGE',
            datetime.date(2020, 3, 20),
        ),
        (
            'MMNT-010',
            '看來很潮實際卻超害羞&hellip; 性愛偏差値MAX辣妹AV出道 寺田心乃',
            '看來很潮實際卻超害羞… 超能幹的辣妹寺田心乃AV出道！很能潮吹外還很能吹，G奶',
            ['潮吹', '巨乳', '中文字幕', 'AV女優片', '出道作', '3P'],
            'K.M.P.',
            datetime.date(2021, 8, 13),
        ),
        (
            'IPX-292',
            '巨乳少妻被討厭的前男友幹到高潮&hellip; 櫻空桃',
            '我與小桃結婚兩年了，對小桃一見鍾情後就求婚了，想說以後就是我的人了…。可是我居然看到她和前男友做愛高潮連連，從未見過的妻子淫蕩姿態，讓我的肉棒不爭氣的勃起了…。',
            ['巨乳', '中文字幕', '乳交', '新娘、少婦', 'AV女優片', '窈窕', '寢取', 'HD高畫質'],
            'IDEA POCKET',
            datetime.date(2019, 4, 13),
        ),
        (
            'CEMD-011',
            '肉棒壞掉5秒前！毫不留情玩弄全套癡女性愛 辻井穗乃果',
            '說著對口交有自信，拍過一百片以上的人氣AV女優辻井穗乃果，自己拿著假屌抽插私處身體扭捏！展現多樣情境玩法！',
            ['熟女', '癡女', '巨乳', '口交', 'AV女優片', '淫亂'],
            'セレブの友',
            datetime.date(2021, 5, 25),
        ),
        (
            'CJOD-278',
            '肛門看透透的W巨臀男性按摩 想看著可愛妹子卑猥屁眼持續射精 松本一香 葵玲奈',
            '可愛的妹子屁眼也很可愛！連屁眼皺褶都看得一清二楚！兩位可愛按摩妹展開多樣屁眼玩法！千萬別錯過！',
            ['中出', '姐姐系', '美容院', '3P', '過激系'],
            '癡女ヘブン',
            datetime.date(2021, 1, 25),
        ),
    ]
)
def test_metadata(number, title, outline, keywords, studio, release_date, proxies):
    crawler = AirAvCrawler(proxies=proxies)
    metadata = crawler.get_metadata(number)

    assert metadata.runtime is None
    assert metadata.series is None
    assert metadata.director is None
    assert metadata.number == number
    assert metadata.title == title
    assert metadata.outline == outline
    assert metadata.keywords == keywords
    assert metadata.studio == studio
    assert metadata.release_date == release_date
    assert metadata.fanart is not None
    assert metadata.poster is not None
    assert not metadata.stars
    print(metadata)

@pytest.mark.parametrize(
    'number', ['100221_001', 'AVSW-061']
)
def test_metadata_with_nonexitant_number(number):
    crawler = AirAvCrawler()
    metadata = crawler.get_metadata(number)

    assert not metadata.runtime
    assert not metadata.series
    assert not metadata.director
    assert not metadata.title
    assert not metadata.outline
    assert not metadata.keywords
    assert not metadata.stars
    assert not metadata.studio
    assert not metadata.release_date
    assert not metadata.fanart
    assert not metadata.poster
    assert metadata.number == number
    print(metadata)
