from api import PetFriends
from settings import *
import os
import pytest

pf = PetFriends()


@pytest.fixture(autouse=True)
def auth_key():
    """Фикстура для получения auth_key перед каждым тестом"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    return auth_key


@pytest.mark.parametrize("name",
                        [generate_string(255), generate_string(1001), russian_chars(), russian_chars().upper(),
                         chinese_chars(), special_chars(), '123'],
                        ids=['255 symbols', 'more than 1000 symbols', 'russian', 'RUSSIAN', 'chinese', 'specials',
                             'digit'])
@pytest.mark.parametrize("animal_type",
                        [generate_string(255), generate_string(1001), russian_chars(), russian_chars().upper(),
                         chinese_chars(), special_chars(), '123'],
                        ids=['255 symbols', 'more than 1000 symbols', 'russian', 'RUSSIAN', 'chinese', 'specials',
                             'digit'])
@pytest.mark.parametrize("age", ['1'], ids=['min'])
def test_add_new_pet_simple(auth_key, name, animal_type, age):
    """Проверяем создание питомца с различными данными (позитивные тесты)"""

    # Добавляем питомца
    status, result = pf.add_new_pet_simple(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name
    assert result['age'] == age
    assert result['animal_type'] == animal_type


@pytest.mark.parametrize("name", [''], ids=['empty'])
@pytest.mark.parametrize("animal_type", [''], ids=['empty'])
@pytest.mark.parametrize("age",
                        ['', '-1', '0', '100', '1.5', '2147483647', '2147483648', special_chars(), russian_chars(),
                         russian_chars().upper(), chinese_chars()],
                        ids=['empty', 'negative', 'zero', 'greater than max', 'float', 'int_max', 'int_max + 1',
                             'specials', 'russian', 'RUSSIAN', 'chinese'])
def test_add_new_pet_simple_negative(auth_key, name, animal_type, age):
    """Проверяем создание питомца с невалидными данными (негативные тесты)"""

    # Добавляем питомца
    status, result = pf.add_new_pet_simple(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 400


@pytest.mark.parametrize("content_type,accept",
                        [
                            ("application/json", "application/json"),
                            ("application/xml", "application/xml"),
                            ("application/json", "application/xml"),
                            ("application/xml", "application/json"),
                            ("", "application/json"),
                            ("application/json", ""),
                            ("", ""),
                        ],
                        ids=[
                            "json_json",
                            "xml_xml",
                            "json_xml",
                            "xml_json",
                            "empty_json",
                            "json_empty",
                            "empty_empty",
                        ])
def test_add_new_pet_simple_content_types(auth_key, content_type, accept):
    """Проверяем создание питомца с различными типами контента"""

    # Добавляем питомца
    status, result = pf.add_new_pet_simple(auth_key, "TestPet", "Dog", "5", content_type=content_type, accept=accept)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == "TestPet"
    assert result['age'] == "5"
    assert result['animal_type'] == "Dog"


@pytest.mark.parametrize("name", [name1], ids=['valid_name'])
@pytest.mark.parametrize("animal_type", [animal_type1], ids=['valid_animal_type'])
@pytest.mark.parametrize("age", [age1], ids=['valid_age'])
@pytest.mark.parametrize("pet_photo", [pet_photo1], ids=['valid_photo'])
def test_add_new_pet(auth_key, name, animal_type, age, pet_photo):
    """Проверяем создание питомца с фотографией"""

    # Получаем полный путь изображения питомца
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name
    assert result['age'] == str(age)
    assert result['animal_type'] == animal_type
    assert 'pet_photo' in result 