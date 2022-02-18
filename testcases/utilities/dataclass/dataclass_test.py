import pytest

from japanese_media_manager.utilities.dataclass import DataClass
from japanese_media_manager.utilities.dataclass import Field
from japanese_media_manager.utilities.dataclass import List
from japanese_media_manager.utilities.dataclass import TypeMissMatchException
from japanese_media_manager.utilities.dataclass import FieldMissException
from japanese_media_manager.utilities.dataclass import AssertionException

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
    assert employee.educations[0].school == 'jialidun'  # pylint: disable=unsubscriptable-object
    assert employee.educations[0].degree == 'master'  # pylint: disable=unsubscriptable-object

    assert isinstance(repr(employee), str)

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
        Employee(data)
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
    assert employee.company.name == 'jialidun'  # pylint: disable=no-member
    assert employee.company.location == 'anywhere'  # pylint: disable=no-member
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

@pytest.mark.parametrize(
    'data, exception', [
        ({}, "cannot find field age in data = {}"),
        ({'age': 233, 'educations': []}, "cannot find field name in data = {'age': 233, 'educations': []}"),
        ({'age': 233, 'name': 'kinopico', 'educations': [{}]}, "cannot find field degree in data['educations'][0] = {}"),
        ({'age': 233, 'name': 'kinopico'}, "cannot find field educations in data = {'age': 233, 'name': 'kinopico'}"),
    ]
)
def test_field_miss_exception(data, exception):
    with pytest.raises(FieldMissException) as information:
        Employee(data)
    assert str(information.value) == exception

def test_field_with_default():
    class Stuff(DataClass):
        name = Field(type=str)
        age = Field(type=int, default=233)

    stuff = Stuff({'name': 'kinopico'})
    assert stuff.age == 233

def test_field_with_alias():
    class Stuff(DataClass):
        name = Field(type=str)
        age = Field(type=int, default=233, alias='year')

    stuff = Stuff({'name': 'kinopico'})
    assert stuff.year == 233  # pylint: disable=no-member

    stuff = Stuff({'name': 'kinopico', 'year': 18})
    assert stuff.year == 18  # pylint: disable=no-member

def test_assertion_exception():
    with pytest.raises(AssertionException) as information:
        Employee({'name': 'kinopico', 'educations': [], 'age': 8})
    assert 'cannot pass assertion' in str(information.value)
