import os
import pathlib
import pytest

@pytest.fixture(name='file_paths', scope='function')
def _file_paths(directory):
    data = [
        ['IPX-486_C.mp4',],
        ['IPX-643_C.mp4',],
        ['MIDE-876.mp4',],
        ['rbd-978.mp4',],
        ['ssni-011-C.mp4',],
        ['SSIS-328 1080p 架乃ゆら.mp4',],
        ['MILK-118.mp4',],
        ['DV-1302-C.mp4',],
        ['.DS_Store',],
        ['MXGS-861_uncensored.mp4',],
        ['MXGS-709-2K-jianying.mp4',],
        ['adn-382-C.mp4',],
        ['rebd-461.mp4',],
        ['ADN-330_C.mp4',],
        ['MIDE-590.mp4',],
        ['SHKD-964-C.mp4',],
        ['atid-403-C.mp4',],
        ['WANZ-952.mp4',],
        ['DASD-978.mp4',],
        ['MIGD-487-C.mp4',],
        ['mide-285.mp4',],
        ['GTJ-086.mp4',],
        ['BDA-109.mp4',],
        ['PRTD-026.mp4',],
        ['star-972-C.mp4',],
        ['IPX-052', 'ipx00052hhb.mp4',],
        ['IPX-052', 'ipx00052pl.jpg',],
        ['RBD-897 把希崎杰西卡送上奴隶的舞台[高清中文字幕][有码]', 'RBD-897.mp4',],
        ['RBD-897 把希崎杰西卡送上奴隶的舞台[高清中文字幕][有码]', 'cover.jpg',],
        ['RBD-897 把希崎杰西卡送上奴隶的舞台[高清中文字幕][有码]', 'screenshot.jpg',],
        ['Rbd-184', 'RBD-184-C.mp4',],
        ['miaa-584', 'miaa-584.mp4',],
        ['miaa-584', 'miaa-584.mp4.jpg',],
        ['miaa-584', 'miaa584pl.jpg',],
        ['rbd-267', 'rbd-267-C.mp4',],
        ['rbd-830', 'RBD-830-C.mp4',],
        ['STARS-071◎七海缇娜(七海ティナ)93◤190509', 'STARS-071_keyint12.mp4',],
        ['STARS-071◎七海缇娜(七海ティナ)93◤190509', '!★A]STARS-071◎七海缇娜(七海ティナ)93◤190509◇STARS_071_20 (已调整大小).jpg',],
        ['STARS-071◎七海缇娜(七海ティナ)93◤190509', '★★STARS_071_2.jpg',],
        ['STARS-071◎七海缇娜(七海ティナ)93◤190509', '★STARS_071_17.jpg',],
        ['STARS-071◎七海缇娜(七海ティナ)93◤190509', 't.jpg',],
        ['STARS-071◎七海缇娜(七海ティナ)93◤190509', 'STARS_071_S.jpg',],
        ['STARS-071◎七海缇娜(七海ティナ)93◤190509', '★STARS_071_19.jpg',],
        ['STARS-071◎七海缇娜(七海ティナ)93◤190509', 'STARS-071 アイドルハンターにピンサロバイトをネタに脅され輪姦されても心だけは屈しなかったアイドル 七海ティナ.jpg',],
        ['STARS-071◎七海缇娜(七海ティナ)93◤190509', 'j', '★A]STARS-071◎七海缇娜(七海ティナ)93◤190509◇STARS_071_20.jpg',],
        ['STARS-071◎七海缇娜(七海ティナ)93◤190509', 'j', '★STARS-071◎七海缇娜(七海ティナ)93◤190509◇STARS_071_20.jpg',],
        ['STARS-071◎七海缇娜(七海ティナ)93◤190509', 'j', 'STARS_071_13.jpg',],
        ['STARS-071◎七海缇娜(七海ティナ)93◤190509', 'j', 'STARS_071_11.jpg',],
        ['STARS-071◎七海缇娜(七海ティナ)93◤190509', 'j', 'STARS_071_12.jpg',],
        ['STARS-071◎七海缇娜(七海ティナ)93◤190509', 'j', 'STARS_071_9.jpg',],
        ['STARS-071◎七海缇娜(七海ティナ)93◤190509', 'j', 'STARS_071_18.jpg',],
        ['STARS-071◎七海缇娜(七海ティナ)93◤190509', 'j', 'STARS_071_10.jpg',],
        ['STARS-071◎七海缇娜(七海ティナ)93◤190509', 'j', 'STARS_071_6.jpg',],
        ['STARS-071◎七海缇娜(七海ティナ)93◤190509', 'j', 'STARS_071_16.jpg',],
        ['STARS-071◎七海缇娜(七海ティナ)93◤190509', 'j', 'STARS_071_8.jpg',],
        ['STARS-071◎七海缇娜(七海ティナ)93◤190509', 'j', 'STARS_071_14.jpg',],
        ['STARS-071◎七海缇娜(七海ティナ)93◤190509', 'j', 'STARS_071_5.jpg',],
        ['STARS-071◎七海缇娜(七海ティナ)93◤190509', 'j', 'STARS_071_1.jpg',],
        ['STARS-071◎七海缇娜(七海ティナ)93◤190509', 'j', 'STARS_071_3.jpg',],
        ['STARS-071◎七海缇娜(七海ティナ)93◤190509', 'j', 'STARS_071_7.jpg',],
        ['STARS-071◎七海缇娜(七海ティナ)93◤190509', 'j', 'STARS_071_4.jpg',],
        ['STARS-071◎七海缇娜(七海ティナ)93◤190509', 'j', 'STARS_071_15.jpg',],
        ['SOE-579', 'soe00579hhb2.wmv',],
        ['SOE-579', 'soe00579hhb1.wmv',],
        ['ipx-832-C', 'ipx-832-C.mp4',],
        ['ipx-832-C', 'ipx832pl.jpg',],
        ['ipx-832-C', 'ipx-832-C.mp4.jpg',],
        ['hunbl-086', 'hunbl-086.mp4',],
        ['hunbl-086', 'hunbl-086.mp4.jpg',],
        ['hunbl-086', 'hunbl086pl.jpg',],
        ['ssni-966-C', 'ssni-966-C.mp4',],
        ['ssni-966-C', 'ssni966pl.jpg',],
        ['FAX合集Ⅱ', 'FAX-340.mp4',],
        ['FAX合集Ⅱ', 'FAX-318 - [FAプロ 軍隊女体拷問].mp4',],
        ['SOE-166', 'FC2PPV-1569537.mp4',],
        ['SOE-166', 'FC2PPV-1569538.mp4',],
        ['SOE-166', 'FC2PPV-1569538.mp4.jpg',],
        ['SOE-166', 'SOE-166.jpg',],
        ['SOE-166', 'FC2PPV-1569537.mp4.jpg',],
        ['soe-146', 'soe-146-C.mp4',],
        ['ssni-412-C', 'ssni-412-C.mp4',],
        ['ssni-412-C', 'ssni00412pl.jpg',],
        ['rbd-725-C', 'rbd-725-C.mp4',],
        ['tki-007', 'tki-007-C.mp4',],
        ['sma-790', 'sma-790-C.mp4',],
        ['MIDE-611 故意露出内裤诱惑我的妹妹二宫光[高清中文字幕]', 'MIDE-611-C.mp4',],
        ['MIDE-611 故意露出内裤诱惑我的妹妹二宫光[高清中文字幕]', 'screenshot.jpg',],
        ['MIDE-611 故意露出内裤诱惑我的妹妹二宫光[高清中文字幕]', 'cover.jpg',],
        ['ADN-318', 'ADN-318.mp4',],
        ['ADN-318', 'ADN-318.nfo',],
        ['ADN-318', 'ADN-318-fanart.jpg',],
        ['ADN-318', 'ADN-318-poster.jpg',],
        ['ADN-318', 'ADN-318-thumb.jpg',],
        ['adn-272-C', 'adn-272-C.mp4',],
        ['adn-272-C', 'adn00272pl.jpg',],
        ['sspd-160-C', 'sspd-160-C.mp4',],
        ['sspd-160-C', 'sspd-160-C.jpg',],
        ['shkd-858', 'SHKD-858.mp4',],
        ['shkd-986', 'shkd-986.mp4',],
        ['shkd-986', 'shkd-986.mp4.jpg',],
        ['shkd-986', 'shkd986pl.jpg',],
        ['MIGD-779', 'migd00779hhb.wmv',],
        ['kawd00701', 'kawd00701.mp4',],
        ['kawd00701', 'kawd00701.mp4_thumbs.jpg',],
        ['kawd00701', 'kawd00701pl.jpg',],
        ['kawd00701', 'folder.jpg',],
        ['WANZ-705', 'wanz00705hhb.mp4',],
        ['WANZ-705', 'wanz00705pl.jpg',],
        ['dasd00321', 'dasd00321.mp4',],
        ['dasd00321', 'dasd00321.mp4_thumbs.jpg',],
        ['dasd00321', 'dasd00321pl.jpg',],
        ['dasd00321', 'folder.jpg',],
        ['SSNI201-401', '.DS_Store',],
        ['MIGD-724', 'MIGD-724.mp4',],
        ['MIGD-724', 'MIGD-724.mp4.jpg',],
        ['MIGD-724', 'migd00724bodpl.jpg',],
        ['hnd-766', 'hnd-766-C.mp4',],
        ['PRTD-022', 'prtd00022hhb.mp4',],
        ['PRTD-022', 'prtd00022pl.jpg',],
        ['PRTD-002', 'prtd00002hhb.mp4',],
        ['PRTD-002', 'prtd00002pl.jpg',],
        ['GVG-835', 'gvg835.HD.mp4',],
        ['GVG-835', '13gvg835pl.jpg',],
        ['rbk-029', 'rbk-029.mp4',],
        ['rbk-029', 'rbk-029.mp4.jpg',],
        ['rbk-029', 'rbk029pl.jpg',],
        ['ipz-111-C', 'ipz-111-C.mp4',],
        ['MUDR-180', 'MUDR-180.mp4',],
        ['waaa-134-C', 'waaa-134-C.mp4',],
    ]

    file_paths = []
    for item in data:
        file_path = os.path.join(directory, *item)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        pathlib.Path(file_path).touch()
        file_paths.append(file_path)

    yield file_paths
