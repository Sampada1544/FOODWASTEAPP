from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import models

from .forms import RegistrationForm

from donations.models import FoodDonation, FoodRequest


# -----------------------------
# Home Page
# -----------------------------

def home(request):

    return render(
        request,
        'users/home.html'
    )


# -----------------------------
# Register
# -----------------------------

def register(request):

    if request.method == 'POST':

        form = RegistrationForm(request.POST)

        if form.is_valid():

            form.save()

            return redirect('login')

    else:

        form = RegistrationForm()

    return render(
        request,
        'users/register.html',
        {'form': form}
    )


# -----------------------------
# Login
# -----------------------------

def login_view(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            return redirect('dashboard')

        return render(
            request,
            'users/login.html',
            {
                'error': 'Invalid username or password'
            }
        )

    return render(
        request,
        'users/login.html'
    )


# -----------------------------
# Logout
# -----------------------------

def logout_view(request):

    logout(request)

    return redirect('home')


# -----------------------------
# Dashboard
# -----------------------------

@login_required
def dashboard(request):

    profile = request.user.userprofile

    total_donations = FoodDonation.objects.count()

    available_food = FoodDonation.objects.filter(
        status='AVAILABLE'
    ).count()

    total_requests = FoodRequest.objects.count()

    collected_food = FoodDonation.objects.filter(
        status='COLLECTED'
    ).count()

    total_quantity = FoodDonation.objects.aggregate(
        total=models.Sum('quantity')
    )['total'] or 0

    estimated_meals = round(
        total_quantity * 2
    )

    return render(
        request,
        'users/dashboard.html',
        {
            'profile': profile,
            'total_donations': total_donations,
            'available_food': available_food,
            'total_requests': total_requests,
            'collected_food': collected_food,
            'total_quantity': total_quantity,
            'estimated_meals': estimated_meals,
        }
    )