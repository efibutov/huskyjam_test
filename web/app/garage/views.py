from django.shortcuts import render
from .models import Technician, Meeting


def index(request):
    meetings = Meeting.objects.all()

    render(
        request,
        'garage/meeting_form.html',
        context={
            'meetings': meetings
        }
    )
