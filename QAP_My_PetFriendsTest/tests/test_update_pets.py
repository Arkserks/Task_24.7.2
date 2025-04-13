from api import PetFriends
from settings import *
import pytest

pf = PetFriends()


@pytest.fixture(autouse=True)
def auth_key():
    """Фикстура для получения auth_key перед каждым тестом"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    return auth_key


@pytest.fixture
def pet_id(auth_key):
    """Фикстура для получения ID питомца перед тестами обновления"""
    # Получаем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Если список пустой, создаем нового питомца
    if len(my_pets['pets']) == 0:
        _, result = pf.add_new_pet_simple(auth_key, "TestPet", "Dog", "5")
        return result['id']
    else:
        return my_pets['pets'][0]['id']


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
@pytest.mark.parametrize("age", [1], ids=['valid_age'])
def test_update_pet_info(auth_key, pet_id, name, animal_type, age):
    """Проверяем обновление информации о питомце с различными данными (позитивные тесты)"""

    # Обновляем информацию о питомце
    status, result = pf.update_pet_info(auth_key, pet_id, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name
    assert result['age'] == str(age)
    assert result['animal_type'] == animal_type


@pytest.mark.parametrize("name", [''], ids=['empty'])
@pytest.mark.parametrize("animal_type", [''], ids=['empty'])
@pytest.mark.parametrize("age",
                        [-1, 0, 100, 1.5, 2147483647, 2147483648],
                        ids=['negative', 'zero', 'greater than max', 'float', 'int_max', 'int_max + 1'])
def test_update_pet_info_negative(auth_key, pet_id, name, animal_type, age):
    """Проверяем обновление информации о питомце с невалидными данными (негативные тесты)"""

    # Обновляем информацию о питомце
    status, result = pf.update_pet_info(auth_key, pet_id, name, animal_type, age)

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
def test_update_pet_info_content_types(auth_key, pet_id, content_type, accept):
    """Проверяем обновление информации о питомце с различными типами контента"""

    # Обновляем информацию о питомце
    status, result = pf.update_pet_info(auth_key, pet_id, "UpdatedPet", "Cat", 10, content_type=content_type, accept=accept)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == "UpdatedPet"
    assert result['age'] == "10"
    assert result['animal_type'] == "Cat"


@pytest.mark.parametrize("pet_photo", [pet_photo2], ids=['valid_photo'])
def test_add_photo_of_pet(auth_key, pet_id, pet_photo):
    """Проверяем добавление фотографии питомцу"""

    # Получаем полный путь изображения питомца
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Добавляем фотографию питомцу
    status, result = pf.add_photo_of_pet(auth_key, pet_id, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert 'pet_photo' in result
    assert result['pet_photo'] != "" 