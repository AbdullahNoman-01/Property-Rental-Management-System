from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from properties.models import Property, RentalRequest


@login_required
def owner_dashboard(request):
    # Owner-er properties
    properties = Property.objects.filter(owner=request.user)

    # Owner-er properties-er rental requests
    rental_requests = RentalRequest.objects.filter(
        property__owner=request.user
    )

    context = {
        # Property statistics
        'total_properties': properties.count(),
        'available_properties': properties.filter(
            availability_status='AVAILABLE'
        ).count(),

        # Rental request statistics
        'total_requests': rental_requests.count(),
        'pending_requests': rental_requests.filter(
            status='PENDING'
        ).count(),
        'accepted_requests': rental_requests.filter(
            status='ACCEPTED'
        ).count(),

        # Management data
        'properties': properties,
        'rental_requests': rental_requests.select_related(
            'tenant',
            'property'
        ),
    }

    return render(
        request,
        'dashboard/owner_dashboard.html',
        context
    )


@login_required
def tenant_dashboard(request):
    # Tenant-er rental requests
    rental_requests = RentalRequest.objects.filter(
        tenant=request.user
    ).select_related('property', 'property__owner')

    context = {
        # Rental request statistics
        'total_requests': rental_requests.count(),

        'pending_requests': rental_requests.filter(
            status='PENDING'
        ).count(),

        'accepted_requests': rental_requests.filter(
            status='ACCEPTED'
        ).count(),

        'rejected_requests': rental_requests.filter(
            status='REJECTED'
        ).count(),

        # Management data
        'rental_requests': rental_requests,
    }

    return render(
        request,
        'dashboard/tenant_dashboard.html',
        context
    )