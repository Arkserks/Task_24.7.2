import os
import random
import string

from dotenv import load_dotenv

load_dotenv()



valid_email = os.getenv('valid_email')
valid_password = os.getenv('valid_password')

invalid_email = os.getenv('invalid_email')
invalid_password = os.getenv('invalid_password')

name1 = 'Shavka'
animal_type1 = 'Lion'
age1 = 33
pet_photo1 = 'images/image2.jpg'

name2 = 'Lola'
animal_type2 = 'Zubr'
age2 = 55
pet_photo2 = 'images/image3.jpg'

pet_photo3 = 'images/The_Office.torrent' #incorrect type of photo

name49 = 'cTxBDH0IbZqKicPFhL8y23UJLIyB59S3p1hqVIa3nYjSZKdr8'
name50 = 'Haxqfifg6HGZJB0jUuEEF13yFlPOIDKvM5vrEUvh24PS0AJLwH' #name consists of 50 characters
name51 = 'o1PsDwg5uo7BHXswSBTuVSxRHUxiVc0LDqlcSFLlP77Z56vv6dE'
name99 = 'CSZtF6PimnEhEYp73kMMZklJvN9JJfUFLeSTzGpghwHSPP3trCKsGzuzr8ilfmoX1Za09SyocelrwCuVxMnW6ThQZbjkpwTKXpA'
name100 = 'EJGwJmLE0y0DhX5soerQOUgx6ixV8aaoRDnkLvmrzI5do8TRNT97QwtxqcQPeLf3JP133tNglPgKodiYbvimt0WPJ9HFkX14wxMO'
name101 = '2khkqZoqSqX3OY96FnBbqi5MvN1EnPkiDckXnjiBbyqB9SeRnjKnH3f0naLghCpoNBeQe9I6K7GuP0ZLR6ibcDvudZDAowdTvvDCG'
name_empty = ''

# Функция для генерации случайной строки заданной длины
def generate_string(n):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=n))

# Функция для генерации строки с русскими символами
def russian_chars():
    return 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'

# Функция для генерации строки с китайскими символами
def chinese_chars():
    return '的一是不了人我在有他这为之大来以个中上们'

# Функция для генерации строки со специальными символами
def special_chars():
    return '|/!@#$%^&*()-_=+`~?"№;:[]{}'