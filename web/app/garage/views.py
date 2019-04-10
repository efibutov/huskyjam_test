from django.forms import ModelForm
from django import forms
from django.shortcuts import render
from .models import Meeting
from .exceptions import DatePassed, NotWorkingHours, DayOff, AlreadyTaken


class MeetingForm(ModelForm):
    class Meta:
        model = Meeting
        fields = (
            'client_first_name',
            'client_last_name',
            'client_patronymic_name',
            'car_model',
            'technician',
            'date',
        )


def index(request):
    errors = None

    if request.method == 'GET':
        form = MeetingForm()
    elif request.method == 'POST':
        form = MeetingForm(request.POST)

        try:
            form.save()
        except (DatePassed, NotWorkingHours, DayOff, AlreadyTaken) as e:
            errors = [e.__class__.__name__]
        else:
            return render(
                request,
                'garage/meeting_info.html',
            )

    return render(
        request,
        'garage/meeting_form.html',
        {
            'form': form,
            'errors': errors
        }
    )
