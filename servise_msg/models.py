import pytz
from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone

SENT = 'Отправлено'
NO_SENT = 'Не отправлено'

STATUS_CHOICES = [
    (SENT, 'Отправлено'),
    (NO_SENT, 'Ожидает отправки'),
]


class Mailing(models.Model):
    start_mailing = models.DateTimeField(verbose_name='Начало рассылки')
    end_mailing = models.DateTimeField(verbose_name='Окончание рассылки')
    text = models.TextField(verbose_name='Текст сообщения')
    mobile_codes = models.CharField(verbose_name='Коды мобильных операторов',
                                    max_length=50,
                                    blank=True)
    tags = models.CharField('Тэги для поиска', max_length=50, blank=True)

    @property
    def to_send(self):
        now = timezone.now()
        if self.start_mailing <= now <= self.end_mailing:
            return True
        else:
            return False

    def __str__(self):
        return f'Рассылка {self.id} от {self.start_mailing}'

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'


class Client(models.Model):
    TIMEZONES = tuple(zip(pytz.all_timezones, pytz.all_timezones))

    phone_regex = RegexValidator(regex=r'^7\w{10}$',
                                 message=('номер телефона клиента в формате '
                                          '7XXXXXXXXXX (X - цифра от 0 до 9)'))
    phone = models.PositiveIntegerField(verbose_name='Мобильный телефон',
                                        validators=[phone_regex],
                                        unique=True)
    code = models.PositiveIntegerField(verbose_name='Код мобильного оператора')
    tag = models.CharField(verbose_name='Тэги для поиска',
                           max_length=50,
                           blank=True)
    time_zone = models.CharField(verbose_name='Часовой пояс', max_length=32,
                                 choices=TIMEZONES, default='UTC')

    def save(self, *args, **kwargs):
        self.code = str(self.phone)[1:4]
        return super(Client, self).save(*args, **kwargs)

    def __str__(self):
        return f'Клиент {self.id} с номером {self.phone}'

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'


class Message(models.Model):
    date_create = models.DateTimeField(verbose_name='Дата и время отправки',
                                       auto_now_add=True)
    status = models.CharField(verbose_name='Статус отправки',
                              max_length=16,
                              choices=STATUS_CHOICES)
    mailing = models.ForeignKey(Mailing,
                                on_delete=models.CASCADE,
                                related_name='messages')
    client = models.ForeignKey(Client,
                               on_delete=models.CASCADE,
                               related_name='messages')

    def __str__(self):
        return (f'Сообщение {self.id} с текстом {self.mailing} '
                f'для {self.client}')

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
