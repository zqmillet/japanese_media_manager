import pytest

from japanese_media_manager.utilities.dataclass import DataClass
from japanese_media_manager.utilities.dataclass import Field
from japanese_media_manager.utilities.dataclass import List
from japanese_media_manager.utilities.dataclass import TypeMissMatchException

class Education(DataClass):
    school = Field(type=str)
    degree = Field(type=str)

class Employee(DataClass):
    name = Field(type=str)
    age = Field(type=int, assertion=lambda x: x > 18)
    educations = List(Education)

def test_dataclass():
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
    assert employee.age == 233
    assert employee.name == 'kinopico'
    assert employee.educations[0].school == 'jialidun'
    assert employee.educations[0].degree == 'master'

    assert repr(employee) == "Employee(name='kinopico', age=233, educations=[Education(school='jialidun', degree='master')])"

@pytest.mark.parametrize(
    'data, exception', [
        (
            {
                'name': 'kinopico',
                'age': '233',
                'educations': [
                    {
                        'school': 'jialidun',
                        'degree': 'master'
                    }
                ]
            },
            "data['age'] = '233', but its type should be int"
        ),
        (
            {
                'name': 'kinopico',
                'age': 233,
                'educations': [
                    {
                        'school': 233,
                        'degree': 'master'
                    }
                ]
            },
            "data['educations'][0]['school'] = 233, but its type should be str"
        )
    ]
)
def test_dataclass_with_type_error(data, exception):
    with pytest.raises(TypeMissMatchException) as information:
        employee = Employee(data)
    assert str(information.value) == exception

def test_nested_classes():
    class Company(DataClass):
        name = Field(type=str)
        location = Field(type=str)

    class Stuff(DataClass):
        name = Field(type=str)
        age = Field(type=int)
        company = Field(type=Company)

    data = {
        'name': 'kinopico',
        'age': 233,
        'company': {
            'name': 'jialidun',
            'location': 'anywhere'
        }
    }

    employee = Stuff(data)
    assert employee.company.name == 'jialidun'
    assert employee.company.location == 'anywhere'
    assert employee.age == 233
    assert employee.name == 'kinopico'

    data = {
        'name': 'kinopico',
        'age': 233,
        'company': {
            'name': 'jialidun',
            'location': None
        }
    }

    with pytest.raises(TypeMissMatchException) as information:
        Stuff(data)

    assert str(information.value) == "data['company']['location'] = None, but its type should be str"
