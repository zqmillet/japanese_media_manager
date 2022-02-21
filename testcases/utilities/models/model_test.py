import sqlalchemy
import sqlalchemy.orm
import datetime
import os
import pytest

from japanese_media_manager.utilities.models import Video
from japanese_media_manager.utilities.models import Star
from japanese_media_manager.utilities.models import Base

@pytest.fixture(name='file_path')
def _file_path():
    file_path = './sqlite.db'
    yield file_path
    if os.path.isfile(file_path):
        os.remove(file_path)

@pytest.fixture(name='session')
def _session(file_path):
    engine = sqlalchemy.create_engine(f'sqlite:///{file_path}')
    session = sqlalchemy.orm.sessionmaker(bind=engine)()

    for name, table in Base.metadata.tables.items():
        table.create(bind=engine)

    yield session

@pytest.mark.parametrize('title', ['gouliguojiashengsiyi'])
@pytest.mark.parametrize('keywords', [['haha', 'hoho'], []])
@pytest.mark.parametrize('series', [None, 'xianggangjizhe'])
@pytest.mark.parametrize('outline', [None, 'weixiaodegongxian'])
@pytest.mark.parametrize('director', [None, 'zhangzhe'])
@pytest.mark.parametrize('length', [{'number': 123, 'unit': 'min'}])
def test_video_model(session, title, keywords, series, outline, director, length):
    video = Video(
        number='star-325',
        title=title,
        keywords=keywords,
        release_date=datetime.datetime.today().date(),
        length=length,
        series=series,
        outline=outline,
        director=director,
    )
    session.add(video)
    session.commit()

    assert session.query(Video).one() is video

