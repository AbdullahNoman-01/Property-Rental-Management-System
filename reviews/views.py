from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from properties.models import Property, RentalRequest
from .models import Review
from .forms import ReviewForm
# Create your views here.

@login_required
def create_review(request, property_id):

    property_obj = get_object_or_404(
        Property,
        id=property_id
    )

    # Only tenant can review
    if request.user.role != 'TENANT':
        messages.error(
            request,
            'Only tenants can submit reviews.'
        )
        return redirect(
            'property_detail',
            pk=property_obj.pk
        )

    # Check accepted rental request
    accepted_request = RentalRequest.objects.filter(
        property=property_obj,
        tenant=request.user,
        status='ACCEPTED'
    ).exists()

    if not accepted_request:
        messages.error(
            request,
            'You can review this property only after your rental request is accepted.'
        )
        return redirect(
            'property_detail',
            pk=property_obj.pk
        )

    # Check existing review
    existing_review = Review.objects.filter(
        property=property_obj,
        tenant=request.user
    ).first()

    if existing_review:
        messages.warning(
            request,
            'You have already reviewed this property.'
        )
        return redirect(
            'property_detail',
            pk=property_obj.pk
        )

    if request.method == 'POST':

        form = ReviewForm(request.POST)

        if form.is_valid():

            review = form.save(commit=False)

            review.tenant = request.user
            review.property = property_obj

            review.save()

            messages.success(
                request,
                'Your review has been submitted successfully.'
            )

            return redirect(
                'property_detail',
                pk=property_obj.pk
            )

    else:
        form = ReviewForm()

    return render(
        request,
        'reviews/create_review.html',
        {
            'form': form,
            'property': property_obj,
        }
    )