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
WORKING_DAYS = (
    ('Понедельник', 1),
    ('Вторник',     2),
    ('Среда',       3),
    ('Четверг',     4),
    ('Пятница',     5),
)


class Technician(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Meeting(models.Model):
    car_model = models.CharField(max_length=50, choices=CAR_MODELS, verbose_name='Марка автомобиля')
    client_first_name = models.CharField(max_length=50, verbose_name='Имя')
    client_last_name = models.CharField(max_length=50, verbose_name='Фамилия')
    client_patronymic_name = models.CharField(max_length=50, verbose_name='Отчество')

    technician = models.ForeignKey(
        Technician, null=True, blank=False, on_delete=models.CASCADE, verbose_name='Выберите специалиста'
    )
    date = models.DateTimeField(null=False, blank=False)

    def __str__(self):
        return f'{self.date}, {self.technician}, {self.client_first_name}, {self.client_last_name}, {self.car_model}'

    def save(self, *args, **kwargs):
        print(f'\n\n\n\nSAVING!!!\n{args}\n{kwargs}\n')
        print('\n\n\n\nSAVING!!!\n\n\n')
        weekday = self.date.isoweekday()

        if weekday not in (d[1] for d in WORKING_DAYS):
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


