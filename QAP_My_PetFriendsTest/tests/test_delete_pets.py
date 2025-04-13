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
    """Фикстура для получения ID питомца перед тестами удаления"""
    # Получаем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Если список пустой, создаем нового питомца
    if len(my_pets['pets']) == 0:
        _, result = pf.add_new_pet_simple(auth_key, "TestPet", "Dog", "5")
        return result['id']
    else:
        return my_pets['pets'][0]['id']


def test_successful_delete_self_pet(auth_key, pet_id):
    """Проверяем возможность удаления питомца"""

    # Удаляем питомца
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200

    # Проверяем, что питомец удален
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    pet_ids = [pet['id'] for pet in my_pets['pets']]
    assert pet_id not in pet_ids


@pytest.mark.parametrize("pet_id", ["invalid_id", "123456789", "0", "-1", ""], ids=['invalid_id', 'random_id', 'zero', 'negative', 'empty'])
def test_delete_pet_negative(auth_key, pet_id):
    """Проверяем удаление питомца с невалидным ID (негативные тесты)"""

    # Удаляем питомца
    status, _ = pf.delete_pet(auth_key, pet_id)

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
def test_delete_pet_content_types(auth_key, pet_id, content_type, accept):
    """Проверяем удаление питомца с различными типами контента"""

    # Удаляем питомца
    status, _ = pf.delete_pet(auth_key, pet_id, content_type=content_type, accept=accept)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200

    # Проверяем, что питомец удален
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    pet_ids = [pet['id'] for pet in my_pets['pets']]
    assert pet_id not in pet_ids 