from django.shortcuts import render, redirect
from .forms import RegisterForm, LoginForm, ProfileUpdateForm
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful! You can now login.')
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {
        'form': form
    })

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {
        'form': form
    })


def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def profile_view(request):
    return render(
        request,
        'accounts/profile.html'
    )

@login_required
def profile_update_view(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(
            request.POST,
            request.FILES,
            instance=request.user
        )
        if form.is_valid():
            form.save()
            messages.success(
                request,
                'Your profile has been updated successfully.'
            )
            return redirect('profile')
    else:
        form = ProfileUpdateForm(
            instance=request.user
        )
    return render(
        request,
        'accounts/profile_update.html',
        {'form': form}
    )