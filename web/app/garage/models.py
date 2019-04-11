from django.db import models
from django.utils import timezone
from .exceptions import DatePassed, NotWorkingHours, DayOff, AlreadyTaken


CAR_MODELS = (
        ('Toyota',      'Toyota'),
        ('Mazda',       'Mazda'),
        ('Hyundai',     'Hyundai'),
        ('Honda',       'Honda'),
        ('Buick',       'Buick'),
    )
WORKING_HOURS = list(range(10, 23))
WORKING_DAYS = {
    1: 'Понедельник',
    2: 'Вторник',
    3: 'Среда',
    4: 'Четверг',
    5: 'Пятница',
}


class Technician(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Meeting(models.Model):
    car_model = models.CharField(max_length=50, choices=CAR_MODELS, verbose_name='Марка автомобиля')
    client_first_name = models.CharField(max_length=50, verbose_name='Имя')
    client_last_name = models.CharField(max_length=50, verbose_name='Фамилия')
    client_patronymic_name = models.CharField(max_length=50, verbose_name='Отчество', blank=True)

    technician = models.ForeignKey(
        Technician, null=True, blank=False, on_delete=models.CASCADE, verbose_name='Выберите специалиста'
    )
    date = models.DateTimeField(null=False, blank=False)

    def __str__(self):
        return f'{self.date}, {self.technician}, {self.client_first_name}, {self.client_last_name}, {self.car_model}'

    def save(self, *args, **kwargs):
        weekday = self.date.isoweekday()

        if weekday not in WORKING_DAYS:
            raise DayOff()

        now = timezone.now()

        if now > self.date:
            raise DatePassed()

        if self.date.hour not in WORKING_HOURS[:-1]:
            raise NotWorkingHours()

        for meeting in self.technician.meeting_set.all():
            if self.date.year == meeting.date.year and \
                    self.date.month == meeting.date.month and \
                    self.date.day == meeting.date.day and \
                    self.date.hour == meeting.date.hour:
                raise AlreadyTaken()

        super().save(*args, **kwargs)
