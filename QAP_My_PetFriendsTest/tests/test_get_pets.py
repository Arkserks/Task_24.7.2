from api import PetFriends
from settings import *
import pytest

pf = PetFriends()


@pytest.fixture(autouse=True)
def auth_key():
    """Фикстура для получения auth_key перед каждым тестом"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    return auth_key


@pytest.mark.parametrize("filter,expected_status",
                        [
                            ("", 200),
                            ("my_pets", 200),
                            ("all_pets", 200),
                            ("invalid_filter", 400),
                        ],
                        ids=[
                            "empty_filter",
                            "my_pets_filter",
                            "all_pets_filter",
                            "invalid_filter",
                        ])
def test_get_list_of_pets(auth_key, filter, expected_status):
    """Проверяем получение списка питомцев с различными фильтрами"""

    # Запрашиваем список питомцев
    status, result = pf.get_list_of_pets(auth_key, filter)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == expected_status
    if expected_status == 200:
        assert 'pets' in result
        assert isinstance(result['pets'], list)


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
def test_get_list_of_pets_content_types(auth_key, content_type, accept):
    """Проверяем получение списка питомцев с различными типами контента"""

    # Запрашиваем список питомцев
    status, result = pf.get_list_of_pets(auth_key, "", content_type=content_type, accept=accept)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 200
    assert 'pets' in result
    assert isinstance(result['pets'], list)


def test_get_empty_list_of_my_pets_after_delete_all(auth_key):
    """Проверяем получение пустого списка питомцев после удаления всех питомцев"""

    # Запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Если список не пустой, удаляем всех питомцев
    if len(my_pets['pets']) > 0:
        for pet in my_pets['pets']:
            pf.delete_pet(auth_key, pet['id'])

    # Запрашиваем список своих питомцев снова
    status, result = pf.get_list_of_pets(auth_key, "my_pets")

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 200
    assert 'pets' in result
    assert isinstance(result['pets'], list)
    assert len(result['pets']) == 0 