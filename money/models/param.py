from django.db import models


class Param(models.Model):
    class Meta:
        verbose_name = 'Параметр'
        verbose_name_plural = 'Параметры'

    title = models.CharField(max_length=256, verbose_name='Название')
    key = models.CharField(max_length=256, verbose_name='Ключ')
    value = models.CharField(max_length=512, verbose_name='Значение')

    @staticmethod
    def get_params():
        params = {}
        items = Param.objects.all()

        for item in items:
            params[item.key] = item.value

        return params

    @staticmethod
    def get_param(key):
        params = Param.get_params()
        if params[key]:
            return params[key]

        return None
