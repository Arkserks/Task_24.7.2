from api import PetFriends
from settings import *
import pytest

pf = PetFriends()


@pytest.mark.parametrize("email,password,expected_status",
                        [
                            (valid_email, valid_password, 200),
                            (invalid_email, valid_password, 403),
                            (valid_email, invalid_password, 403),
                            (invalid_email, invalid_password, 403),
                            ("", valid_password, 403),
                            (valid_email, "", 403),
                            ("", "", 403),
                            ("test@test.com", "password", 403),
                            ("test@test.com", "123456", 403),
                            ("test@test.com", "", 403),
                            ("", "password", 403),
                        ],
                        ids=[
                            "valid_credentials",
                            "invalid_email",
                            "invalid_password",
                            "invalid_credentials",
                            "empty_email",
                            "empty_password",
                            "empty_credentials",
                            "random_email_valid_password",
                            "random_email_invalid_password",
                            "random_email_empty_password",
                            "empty_email_random_password",
                        ])
def test_get_api_key(email, password, expected_status):
    """Проверяем получение API ключа с различными комбинациями email и password"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == expected_status
    if expected_status == 200:
        assert 'key' in result
    else:
        assert 'key' not in result


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
def test_get_api_key_content_types(content_type, accept):
    """Проверяем получение API ключа с различными типами контента"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(valid_email, valid_password, content_type=content_type, accept=accept)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 200
    assert 'key' in result 