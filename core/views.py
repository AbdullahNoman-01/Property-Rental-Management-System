from django.shortcuts import render
from properties.models import Property


def home(request):
    properties = Property.objects.select_related('owner').filter(
        availability_status='AVAILABLE'
    )

    context = {
        'properties': properties,
    }

    return render(
        request,
        'home.html',
        context
    )