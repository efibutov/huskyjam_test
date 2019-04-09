from django.db import models
CAR_MODELS = (
        ('Toyota',      'Toyota'),
        ('Mazda',       'Mazda'),
        ('Hyundai',     'Hyundai'),
        ('Honda',       'Honda'),
        ('Buick',       'Buick'),
    )
WORKING_HOURS = ((hr, hr) for hr in range(10, 23))
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
    car_model = models.CharField(max_length=50, choices=CAR_MODELS)
    client_first_name = models.CharField(max_length=50)
    client_last_name = models.CharField(max_length=50)

    technician = models.ForeignKey(Technician, null=True, blank=False, on_delete=models.CASCADE, related_name='meeting')
    date_time = models.DateTimeField(null=False, blank=False)

    def __str__(self):
        return f'{self.date_time}'

    def save(self, *args, **kwargs):
        print(self.technician)
        super().save(*args, **kwargs)
