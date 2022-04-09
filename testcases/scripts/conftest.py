import os
import pathlib
import pytest

@pytest.fixture(name='file_paths', scope='function')
def _file_paths(directory):
    data = [
        ['IPX.mp4'],
        ['gouliguojiashengsiyi-1926.mp4'],
        ['IPX-486_C.mp4'],
        ['IPX-643_C.mp4'],
        ['MIDE-876.mp4'],
        ['ssni-011-C.mp4'],
        ['SSIS-328 1080p 架乃ゆら.mp4'],
        ['MXGS-861_uncensored.mp4'],
        ['MXGS-709-2K-jianying.mp4'],
        ['IPX-052', 'ipx00052hhb.mp4'],
        ['IPX-052', 'ipx00052pl.jpg'],
        ['RBD-897 把希崎杰西卡送上奴隶的舞台[高清中文字幕][有码]', 'RBD-897.mp4'],
        ['RBD-897 把希崎杰西卡送上奴隶的舞台[高清中文字幕][有码]', 'cover.jpg'],
        ['RBD-897 把希崎杰西卡送上奴隶的舞台[高清中文字幕][有码]', 'screenshot.jpg'],
        ['STARS-071◎七海缇娜(七海ティナ)93◤190509', 'STARS-071_keyint12.mp4'],
        ['STARS-071◎七海缇娜(七海ティナ)93◤190509', '!★A]STARS-071◎七海缇娜(七海ティナ)93◤190509◇STARS_071_20 (已调整大小).jpg'],
        ['STARS-071◎七海缇娜(七海ティナ)93◤190509', 't.jpg'],
        ['STARS-071◎七海缇娜(七海ティナ)93◤190509', 'STARS_071_S.jpg'],
        ['STARS-071◎七海缇娜(七海ティナ)93◤190509', '★STARS_071_19.jpg'],
        ['STARS-071◎七海缇娜(七海ティナ)93◤190509', 'j', '★A]STARS-071◎七海缇娜(七海ティナ)93◤190509◇STARS_071_20.jpg'],
        ['STARS-071◎七海缇娜(七海ティナ)93◤190509', 'j', '★STARS-071◎七海缇娜(七海ティナ)93◤190509◇STARS_071_20.jpg'],
        ['STARS-071◎七海缇娜(七海ティナ)93◤190509', 'j', 'STARS_071_13.jpg'],
        ['STARS-071◎七海缇娜(七海ティナ)93◤190509', 'j', 'STARS_071_11.jpg'],
        ['STARS-071◎七海缇娜(七海ティナ)93◤190509', 'j', 'STARS_071_12.jpg'],
        ['STARS-071◎七海缇娜(七海ティナ)93◤190509', 'j', 'STARS_071_9.jpg'],
        ['STARS-071◎七海缇娜(七海ティナ)93◤190509', 'j', 'STARS_071_18.jpg'],
        ['STARS-071◎七海缇娜(七海ティナ)93◤190509', 'j', 'STARS_071_10.jpg'],
        ['STARS-071◎七海缇娜(七海ティナ)93◤190509', 'j', 'STARS_071_6.jpg'],
        ['STARS-071◎七海缇娜(七海ティナ)93◤190509', 'j', 'STARS_071_16.jpg'],
        ['STARS-071◎七海缇娜(七海ティナ)93◤190509', 'j', 'STARS_071_8.jpg'],
        ['STARS-071◎七海缇娜(七海ティナ)93◤190509', 'j', 'STARS_071_14.jpg'],
        ['STARS-071◎七海缇娜(七海ティナ)93◤190509', 'j', 'STARS_071_5.jpg'],
        ['STARS-071◎七海缇娜(七海ティナ)93◤190509', 'j', 'STARS_071_1.jpg'],
        ['STARS-071◎七海缇娜(七海ティナ)93◤190509', 'j', 'STARS_071_3.jpg'],
        ['STARS-071◎七海缇娜(七海ティナ)93◤190509', 'j', 'STARS_071_7.jpg'],
        ['STARS-071◎七海缇娜(七海ティナ)93◤190509', 'j', 'STARS_071_4.jpg'],
        ['STARS-071◎七海缇娜(七海ティナ)93◤190509', 'j', 'STARS_071_15.jpg'],
        ['SOE-579', 'soe00579hhb2.wmv'],
        ['SOE-579', 'soe00579hhb1.wmv'],
        ['ipx-832-C', 'ipx832pl.jpg'],
        ['ipx-832-C', 'ipx-832-C.mp4.jpg'],
        ['hunbl-086', 'hunbl-086.mp'],
        ['hunbl-086', 'hunbl-086.mp4.jpg'],
        ['FAX合集Ⅱ', 'FAX-318 - [FAプロ 軍隊女体拷問].mp4'],
        ['ssni-412-C', 'ssni00412pl.jpg'],
        ['SSNI201-401', '.DS_Store'],
        ['MIGD-724', 'MIGD-724.mp4'],
        ['MIGD-724', 'MIGD-724.mp4.jpg'],
        ['MIGD-724', 'migd00724bodpl.jpg'],
        ['hnd-766', 'hnd-766-C.mp4'],
        ['PRTD-022', 'prtd00022hhb.mp4'],
        ['PRTD-022', 'prtd00022pl.jpg'],
        ['PRTD-002', 'prtd00002hhb.mp4'],
        ['PRTD-002', 'prtd00002pl.jpg'],
    ]

    file_paths = []
    for item in data:
        file_path = os.path.join(directory, *item)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        pathlib.Path(file_path).touch()
        file_paths.append(file_path)

    yield file_paths
