from django.test import TestCase
from .models import Meeting, Technician, CAR_MODELS, WORKING_DAYS, WORKING_HOURS
from .exceptions import DatePassed, NotWorkingHours, DayOff, AlreadyTaken
from django.utils import timezone
import datetime


class MeetingTestCase(TestCase):
    def setUp(self):
        self.technician_1 = Technician(first_name='Антон', last_name='Чехов')
        self.technician_1.save()
        self.technician_2 = Technician(first_name='Лев', last_name='Толстой')
        self.technician_2.save()

    def test_create_meeting_success(self):
        # Avoid failing test on DatePassed
        date = timezone.now() + timezone.timedelta(days=1)

        while True:
            weekday = date.isoweekday()

            # Set meeting day in first closest working day
            if weekday in WORKING_DAYS:
                date = datetime.datetime(
                    year=date.year, month=date.month, day=date.day, hour=10
                )
                break

            date = date + timezone.timedelta(days=1)

        meeting = Meeting(
            car_model=CAR_MODELS[0][0],
            client_first_name='Михаил',
            client_last_name='Горбачёв',
            technician=self.technician_1,
            date=date
        )
        meeting.save()
        self.assertIsNotNone(meeting.pk)

        meeting = Meeting(
            car_model=CAR_MODELS[0][0],
            client_first_name='Никита',
            client_last_name='Хрущёв',
            technician=self.technician_2,
            date=date
        )
        meeting.save()
        self.assertIsNotNone(meeting.pk)

    def test_fail_create_meeting_day_off(self):
        def create_meeting_day_off():
            # Set meeting on day off
            date = timezone.now()

            while True:
                weekday = date.isoweekday()

                if weekday not in WORKING_DAYS:
                    date = datetime.datetime(
                        year=date.year, month=date.month, day=date.day, hour=10
                    )
                    break

                date = date + timezone.timedelta(days=1)

            Meeting(
                car_model=CAR_MODELS[0][0],
                client_first_name='Михаил',
                client_last_name='Горбачёв',
                technician=self.technician_1,
                date=date
            ).save()

        self.assertRaises(DayOff, create_meeting_day_off)

    def test_fail_create_meeting_not_working_hours(self):
        def create_meeting_not_working_hours(hour):
            date = timezone.now() + timezone.timedelta(days=1)

            while True:
                weekday = date.isoweekday()

                # Set meeting day in first closest working day
                if weekday in WORKING_DAYS:
                    date = datetime.datetime(
                        year=date.year, month=date.month, day=date.day, hour=hour
                    )
                    break

                date = date + timezone.timedelta(days=1)

            Meeting(
                car_model=CAR_MODELS[0][0],
                client_first_name='Михаил',
                client_last_name='Горбачёв',
                technician=self.technician_1,
                date=datetime.datetime(
                    year=date.year, month=date.month, day=date.day, hour=date.hour
                )
            ).save()

        for hr in [_ for _ in range(0, 24) if _ not in WORKING_HOURS]:
            self.assertRaises(NotWorkingHours, create_meeting_not_working_hours, hr)

    def test_fail_create_meeting_date_passed(self):
        def create_meeting_date_passed():
            Meeting(
                car_model=CAR_MODELS[0][0],
                client_first_name='Михаил',
                client_last_name='Горбачёв',
                technician=self.technician_1,
                date=timezone.now()
            ).save()

        self.assertRaises(DatePassed, create_meeting_date_passed)

    def test_fail_already_taken(self):
        def create_meeting_already_taken():
            # Avoid failing test on DatePassed
            date = timezone.now() + timezone.timedelta(days=1)

            while True:
                weekday = date.isoweekday()

                # Set meeting day in first closest working day
                if weekday in WORKING_DAYS:
                    date = datetime.datetime(
                        year=date.year, month=date.month, day=date.day, hour=10
                    )
                    break

                date = date + timezone.timedelta(days=1)

            meeting = Meeting(
                car_model=CAR_MODELS[0][0],
                client_first_name='Михаил',
                client_last_name='Горбачёв',
                technician=self.technician_1,
                date=date
            )
            meeting.save()
            self.assertIsNotNone(meeting.pk)

            Meeting(
                car_model=CAR_MODELS[1][0],
                client_first_name='Никита',
                client_last_name='Хрущёв',
                technician=self.technician_1,
                date=date
            ).save()

        self.assertRaises(AlreadyTaken, create_meeting_already_taken)
