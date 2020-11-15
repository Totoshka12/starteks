from __future__ import unicode_literals

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    CLIENT = 1
    MANAGER = 2

    ROLE_CHOICES = (
        (CLIENT, 'Клиент'),
        (MANAGER, 'Менеджер'),
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    email = models.EmailField(_('email address'), unique=True)
    patronymic_name = models.CharField(verbose_name='Отчество', max_length=255, blank=True, default='')
    address = models.CharField(verbose_name='Адрес доставки', max_length=255, blank=True, default='')
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, default=CLIENT)

    def full_name(self):
        return '{} {} {}'.format(self.last_name, self.first_name, self.patronymic_name)

    def is_client(self):
        return self.role == self.CLIENT

    def is_manager(self):
        return self.role == self.MANAGER

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
