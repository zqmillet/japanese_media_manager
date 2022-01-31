from japanese_media_manager.utilities.dataclass import DataClass
from japanese_media_manager.utilities.dataclass import Field
from japanese_media_manager.utilities.dataclass import List

def test_dataclass():
    class Education(DataClass):
        school = Field(type=str)
        degree = Field(type=str)

    class Employee(DataClass):
        name = Field(type=str)
        age = Field(type=int, assertion=lambda x: x > 18)
        educations = List(Education)

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
