from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse

from .forms import CampaignRequestForm


def advertise_view(request):
    campaign_success = request.session.pop('campaign_request_success', False)

    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.error(
                request,
                'Please create an account or connect (log in) before submitting your campaign request.'
            )
            login_url = f"{reverse('login')}?next={reverse('advertise:advertise')}#promote-form"
            return redirect(login_url)

        form = CampaignRequestForm(request.POST)
        if form.is_valid():
            campaign_request = form.save(commit=False)
            campaign_request.user = request.user
            campaign_request.save()
            request.session['campaign_request_success'] = True
            return redirect('advertise:advertise')
    else:
        initial_data = {}
        if request.user.is_authenticated:
            name = request.user.get_full_name() or request.user.username
            phone = getattr(request.user, 'phone', '')
            initial_data['full_name'] = name
            if phone:
                initial_data['phone_number'] = phone

        form = CampaignRequestForm(initial=initial_data)

    return render(
        request,
        'advertise/advertise.html',
        {
            'form': form,
            'campaign_success': campaign_success,
        },
    )

