from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Property, RentalRequest , Notification
from reviews.models import Review
from .forms import PropertyForm, RentalRequestForm
from django.contrib import messages

from django.db.models import Q


@login_required
def property_list(request):
    properties = Property.objects.select_related('owner')

    # Search by property title or location
    search_query = request.GET.get('search_query', '').strip()

    if search_query:
        properties = properties.filter(
            Q(title__icontains=search_query) |
            Q(location__icontains=search_query)
        )
    # Property type filter
    property_type = request.GET.get('property_type', '').strip()

    if property_type:
        properties = properties.filter(
            property_type=property_type
        )
    # Minimum rent filter
    min_price = request.GET.get('min_price', '').strip()
    if min_price:
        properties = properties.filter(
            monthly_rent__gte=min_price
        )
    # Maximum rent filter
    max_price = request.GET.get('max_price', '').strip()
    if max_price:
        properties = properties.filter(
            monthly_rent__lte=max_price
        )
    context = {
        'properties': properties,
        'search_query': search_query,
        'selected_property_type': property_type,
        'min_price': min_price,
        'max_price': max_price,
    }
    return render(
        request,
        'properties/property_list.html',
        context
    )


@login_required
def property_detail(request, pk):

    property = get_object_or_404(
        Property.objects.select_related('owner'),
        pk=pk
    )

    reviews = Review.objects.filter(
        property=property
    ).select_related('tenant')

    can_review = False

    if request.user.role == 'TENANT':

        accepted_request = RentalRequest.objects.filter(
            property=property,
            tenant=request.user,
            status='ACCEPTED'
        ).exists()

        already_reviewed = Review.objects.filter(
            property=property,
            tenant=request.user
        ).exists()

        can_review = (
            accepted_request and
            not already_reviewed
        )

    return render(
        request,
        'properties/property_details.html',
        {
            'property': property,
            'reviews': reviews,
            'can_review': can_review,
        }
    )


@login_required
def property_create(request):
    if request.user.role != "OWNER":
        messages.error(
            request,
            "Only property owners can access this page."
        )
        return redirect("property_list")
    
    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES)

        if form.is_valid():
            property = form.save(commit=False)
            property.owner = request.user
            property.save()
            messages.success(
                request,
                'Property has been added successfully! 🎉'
            )
            return redirect('property_list')

    else:
        form = PropertyForm()

    return render(
        request,
        'properties/property_form.html',
        {'form': form}
    )


@login_required
def property_update(request, pk):

    property = get_object_or_404(Property, pk=pk)

    # Only owner can edit
    if property.owner != request.user:
        messages.error(
            request,
            'You are not allowed to edit this property.'
        )
        return redirect('property_detail', pk=property.pk)

    if request.method == 'POST':
        form = PropertyForm(
            request.POST,
            request.FILES,
            instance=property
        )

        if form.is_valid():
            form.save()
            messages.success(
                request,
                'Property has been updated successfully! ✨'
            )
            return redirect(
                'property_detail',
                pk=property.pk
            )

    else:
        form = PropertyForm(instance=property)

    return render(
        request,
        'properties/property_form.html',
        {
            'form': form,
            'property': property
        }
    )


@login_required
def property_delete(request, pk):

    property = get_object_or_404(Property, pk=pk)

    # Only owner can delete
    if property.owner != request.user:
        messages.error(
            request,
            'You are not allowed to delete this property.'
        )
        return redirect('property_detail', pk=property.pk)

    if request.method == 'POST':
        property.delete()
        messages.success(
            request,
            'Property has been deleted successfully.'
        )
        return redirect('property_list')

    return render(
        request,
        'properties/property_confirm_delete.html',
        {'property': property}
    )


@login_required
def create_rental_request(request, property_id):

    property = get_object_or_404(
        Property,
        id=property_id
    )

    # Property available kina
    if property.availability_status != 'AVAILABLE':
        messages.error(
            request,
            'This property is currently not available.'
        )
        return redirect('property_detail', pk=property.pk)

    # Owner nijer property-te request krte parbe na
    if property.owner == request.user:
        messages.error(
            request,
            'You cannot send a rental request for your own property.'
        )
        return redirect('property_detail', pk=property.pk)

    # Already pending request ase kina
    existing_request = RentalRequest.objects.filter(
        property=property,
        tenant=request.user,
        status='PENDING'
    ).exists()

    if existing_request:
        messages.warning(
            request,
            'You already have a pending request for this property.'
        )
        return redirect('property_detail', pk=property.pk)

    if request.method == 'POST':

        form = RentalRequestForm(request.POST)

        if form.is_valid():

            rental_request = form.save(commit=False)

            rental_request.property = property
            rental_request.tenant = request.user
            rental_request.status = 'PENDING'

            rental_request.save()
            Notification.objects.create(
                recipient=property.owner,
                sender=request.user,
                rental_request=rental_request,
                notification_type='NEW_REQUEST',
                message=f'{request.user.username} sent a rental request for {property.title}.'
            )

            messages.success(
                request,
                'Rental request sent successfully.'
            )

            return redirect('my_rental_requests')

    else:
        form = RentalRequestForm()

    context = {
        'form': form,
        'property': property,
    }

    return render(
        request,
        'rental_requests/create_request.html',
        context
    )


@login_required
def my_rental_requests(request):

    rental_requests = RentalRequest.objects.filter(
        tenant=request.user
    ).exclude(
        status='CANCELLED'
    ).select_related('property')

    context = {
        'rental_requests': rental_requests,
    }

    return render(
        request,
        'rental_requests/my_requests.html',
        context
    )


@login_required
def cancel_rental_request(request, request_id):

    rental_request = get_object_or_404(
        RentalRequest,
        id=request_id,
        tenant=request.user
    )

    if rental_request.status != 'PENDING':
        messages.error(
            request,
            'Only pending requests can be cancelled.'
        )
        return redirect('my_rental_requests')

    rental_request.status = 'CANCELLED'
    rental_request.save()

    Notification.objects.create(
        recipient=rental_request.property.owner,
        sender=request.user,
        rental_request=rental_request,
        notification_type='REQUEST_CANCELLED',
        message=f'{request.user.username} cancelled the rental request for {rental_request.property.title}.'
    )

    messages.success(
        request,
        'Rental request cancelled successfully.'
    )

    return redirect('my_rental_requests')


@login_required
def owner_rental_requests(request):

    rental_requests = RentalRequest.objects.filter(
        property__owner=request.user
    ).exclude(
        status='CANCELLED'
    ).select_related(
        'property',
        'tenant'
    )

    context = {
        'rental_requests': rental_requests,
    }

    return render(
        request,
        'rental_requests/owner_requests.html',
        context
    )


@login_required
def accept_rental_request(request, request_id):

    rental_request = get_object_or_404(
        RentalRequest,
        id=request_id,
        property__owner=request.user
    )

    if rental_request.status != 'PENDING':
        messages.error(
            request,
            'Only pending requests can be accepted.'
        )
        return redirect('owner_rental_requests')

    rental_request.status = 'ACCEPTED'
    rental_request.save()
    Notification.objects.create(
        recipient=rental_request.tenant,
        sender=request.user,
        rental_request=rental_request,
        notification_type='REQUEST_ACCEPTED',
        message=f'Your rental request for {rental_request.property.title} has been accepted.'
    )

    messages.success(
        request,
        'Rental request accepted successfully.'
    )

    return redirect('owner_rental_requests')


@login_required
def reject_rental_request(request, request_id):

    rental_request = get_object_or_404(
        RentalRequest,
        id=request_id,
        property__owner=request.user
    )

    if rental_request.status != 'PENDING':
        messages.error(
            request,
            'Only pending requests can be rejected.'
        )
        return redirect('owner_rental_requests')

    rental_request.status = 'REJECTED'
    rental_request.save()

    Notification.objects.create(
        recipient=rental_request.tenant,
        sender=request.user,
        rental_request=rental_request,
        notification_type='REQUEST_REJECTED',
        message=f'Your rental request for {rental_request.property.title} has been rejected.'
    )

    messages.success(
        request,
        'Rental request rejected successfully.'
    )

    return redirect('owner_rental_requests')


@login_required
def notifications(request):
    notifications = Notification.objects.filter(
        recipient=request.user
    ).select_related(
        'sender',
        'rental_request',
        'rental_request__property'
    ).order_by('-created_at')

    context = {
        'notifications': notifications,
    }

    return render(
        request,
        'rental_requests/notifications.html',
        context
    )

@login_required
def notification_redirect(request, notification_id):

    notification = get_object_or_404(
        Notification,
        id=notification_id,
        recipient=request.user
    )

    # Notification read করা
    notification.is_read = True
    notification.save(update_fields=['is_read'])

    # Campaign Contacted notification redirect
    if notification.notification_type == 'CAMPAIGN_CONTACTED' or not notification.rental_request:
        return redirect('advertise:advertise')

    # User-এর role অনুযায়ী redirect
    if request.user.role == 'TENANT':
        return redirect('my_rental_requests')

    elif request.user.role == 'OWNER':
        return redirect('owner_rental_requests')

    return redirect('home')


@login_required
def mark_all_notifications_read(request):
    Notification.objects.filter(
        recipient=request.user,
        is_read=False
    ).update(is_read=True)

    return redirect('notifications')