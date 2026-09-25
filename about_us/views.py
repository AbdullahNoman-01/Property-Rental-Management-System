from django.shortcuts import render
from properties.models import Property


def about_us_view(request):
    latest_properties = Property.objects.filter(
        availability_status='AVAILABLE'
    ).select_related('owner').order_by('-created_at')[:9]

    return render(
        request,
        'about_us/about_us.html',
        {
            'latest_properties': latest_properties,
        },
    )

