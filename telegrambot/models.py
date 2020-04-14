from django.db import models


# Профиль
class Profile(models.Model):
    external_id = models.PositiveIntegerField(
        verbose_name='ID пользователя в боте',
        unique=True,
    )
    name = models.TextField(
        verbose_name='Имя пользователя',
    )
    surname = models.TextField(
        verbose_name='Фамилия пользователя',
    )
    number = models.TextField(
        verbose_name='Номер телефона',
    )

    # Метод отображения

    def __str__(self):
        return f'#{self.external_id} {self.name}'

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'


# Бонусы
class Bonus(models.Model):
    profile = models.ForeignKey(
        Profile,
        verbose_name='Профиль',
        on_delete=models.SET_NULL,
        null=True,
    )
    bonus = models.PositiveIntegerField(
        verbose_name='Бонус',
    )

    # Метод отображения
    def __str__(self):
        return f'#Количество {self.bonus} для {self.profile}'

    class Meta:
        verbose_name = 'Бонус'
        verbose_name_plural = 'Бонусы'


class Trip(models.Model):
    departure = models.TextField(
        verbose_name='Место посадки'
    )
    place_of_arrival = models.TextField(
        verbose_name='Место прибытия'
    )
    time_departure = models.DateTimeField(
        verbose_name='Время посадки'
    )
    time_place_of_arrival = models.DateTimeField(
        verbose_name='Время прибытия'
    )
    profile = models.ForeignKey(
        Profile,
        verbose_name='Профиль',
        on_delete=models.SET_NULL,
        null=True,
    )

    def __str__(self):
        return f'#Отправка {self.departure} время {self.time_departure} прибытие {self.place_of_arrival} время {self.time_place_of_arrival}'

    class Meta:
        verbose_name = 'Поездка'
        verbose_name_plural = 'Поездки'
