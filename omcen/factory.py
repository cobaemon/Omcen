from random import randint

from django.contrib.auth import get_user_model
from factory import Faker
from factory.django import DjangoModelFactory

UserModel = get_user_model()
FAKER_LOCALE = 'ja_JP'


class OmcenUserFactory(DjangoModelFactory):
    class Meta:
        model = UserModel

    username = Faker(provider='user_name', locale=FAKER_LOCALE)
    first_name = Faker(provider='first_name', locale=FAKER_LOCALE)
    last_name = Faker(provider='last_name', locale=FAKER_LOCALE)
    password = Faker(provider='lexify', locale=FAKER_LOCALE,
                     text='?' * randint(1, 128),
                     letters='0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ`˜!@#$%^&*()_+-={}[]\|:;"\'<>,.?/')
    email = Faker(provider='safe_email', locale=FAKER_LOCALE)
    is_authenticated = True
