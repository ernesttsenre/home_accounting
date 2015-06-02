from django.apps import AppConfig

class MoneyAppConfig(AppConfig):
    name = 'money'
    verbose_name = 'Деньги'

default_app_config = 'money.MoneyAppConfig'