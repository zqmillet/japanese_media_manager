import typing

from japanese_media_manager.utilities.dataclass import DataClass
from japanese_media_manager.utilities.dataclass import field

def test_dataclass():
    class Education(DataClass):
        school = field(type=str)
        degree = field(type=str)

    class Employee(DataClass):
        name = field(type=str)
        age = field(type=int, assertion=lambda x: x > 18)
        educations = typing.List[Education]

    data = {
        'name': 'kinopico',
        'age': 233,
        'educations': [
            {
                'school': 'jialidun',
                'degree': 'master'
            }
        ]
    }

    employee = Employee(data)
