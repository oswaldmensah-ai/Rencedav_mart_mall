"""
Account views: register, login, logout, profile.
"""

from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.utils.http import url_has_allowed_host_and_scheme

from .forms import UserLoginForm, UserProfileForm, UserRegistrationForm


def register(request):
    if request.user.is_authenticated:
        return redirect('store:home')

    form = UserRegistrationForm(request.POST or None)
    if form.is_valid():
        user = form.save()
        auth.login(request, user)
        messages.success(request, f'Welcome to Rencedav Mart, {user.first_name}!')
        return redirect('store:home')

    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('store:home')

    next_url = request.POST.get('next') or request.GET.get('next')
    form = UserLoginForm(request, data=request.POST or None)
    if form.is_valid():
        auth.login(request, form.get_user())
        messages.success(request, 'Welcome back!')
        if next_url and url_has_allowed_host_and_scheme(next_url, {request.get_host()}):
            return redirect(next_url)
        return redirect('store:home')

    return render(request, 'accounts/login.html', {'form': form, 'next': next_url})


def logout_view(request):
    if request.method == 'POST':
        auth.logout(request)
        messages.info(request, 'You have been signed out.')
    return redirect('store:home')


@login_required
def profile(request):
    form = UserProfileForm(request.POST or None, instance=request.user)
    if form.is_valid():
        form.save()
        messages.success(request, 'Profile updated successfully.')
        return redirect('accounts:profile')

    orders = request.user.order_set.select_related().order_by('-created_at')[:10]
    return render(request, 'accounts/profile.html', {'form': form, 'orders': orders})
