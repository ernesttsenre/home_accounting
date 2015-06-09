from django.db import models


class Category(models.Model):
    class Meta:
        verbose_name = 'Основание'
        verbose_name_plural = 'Основания'
        ordering = ['title']

    title = models.CharField(
        max_length=256,
        verbose_name='Название'
    )

    affected_limit = models.BooleanField(
        verbose_name='Влияет на лимиты?',
        default=True
    )

    created_at = models.DateTimeField(
        verbose_name='Создан',
        auto_now_add=True
    )

    def __str__(self):
        return self.title