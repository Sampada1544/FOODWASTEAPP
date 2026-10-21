from datetime import datetime, date

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

from functools import wraps

from .forms import FoodDonationForm
from .models import FoodDonation, FoodRequest

from ml.predictor import predict_priority


# =========================================================
# ROLE PROTECTION
# =========================================================

def role_required(allowed_roles):

    def decorator(view_func):

        @wraps(view_func)
        def wrapper(request, *args, **kwargs):

            if not request.user.is_authenticated:
                return redirect('login')

            try:
                role = request.user.userprofile.role

            except Exception:
                return HttpResponseForbidden(
                    "User profile not found."
                )

            if role not in allowed_roles:
                return HttpResponseForbidden(
                    "You are not authorized to access this page."
                )

            return view_func(request, *args, **kwargs)

        return wrapper

    return decorator


# =========================================================
# EXPIRED FOOD HANDLING
# =========================================================

def update_expired_donations():

    today = date.today()

    FoodDonation.objects.filter(
        expiry_date__lt=today,
        status='AVAILABLE'
    ).update(
        status='EXPIRED'
    )


# =========================================================
# DONOR - DONATE FOOD
# =========================================================

@login_required
@role_required(['DONOR'])
def donate_food(request):

    if request.method == 'POST':

        form = FoodDonationForm(request.POST)

        if form.is_valid():

            donation = form.save(commit=False)

            donation.donor = request.user

            # Calculate hours until expiry

            expiry_datetime = datetime.combine(
                donation.expiry_date,
                datetime.min.time()
            )

            current_datetime = datetime.now()

            hours_to_expiry = (
                expiry_datetime - current_datetime
            ).total_seconds() / 3600

            # Distance entered by donor

            distance_km = donation.distance_km

            # AI priority prediction

            priority = predict_priority(
                donation.get_food_type_display(),
                donation.quantity,
                hours_to_expiry,
                distance_km
            )

            donation.priority = priority.upper()

            donation.save()

            return redirect('dashboard')

    else:

        form = FoodDonationForm()

    return render(
        request,
        'donations/donate_food.html',
        {'form': form}
    )


# =========================================================
# DONOR - MY DONATIONS
# =========================================================

@login_required
@role_required(['DONOR'])
def my_donations(request):

    donations = FoodDonation.objects.filter(
        donor=request.user
    ).order_by('-created_at')

    return render(
        request,
        'donations/my_donations.html',
        {'donations': donations}
    )


# =========================================================
# NGO - AVAILABLE FOOD
# =========================================================

@login_required
@role_required(['NGO'])
def available_food(request):

    # Update expired donations first

    update_expired_donations()

    donations = FoodDonation.objects.filter(
        status='AVAILABLE'
    ).order_by('-created_at')

    return render(
        request,
        'donations/available_food.html',
        {'donations': donations}
    )


# =========================================================
# NGO - REQUEST FOOD
# =========================================================

@login_required
@role_required(['NGO'])
def request_food(request, donation_id):

    donation = FoodDonation.objects.get(
        id=donation_id
    )

    # Prevent duplicate requests

    existing_request = FoodRequest.objects.filter(
        donation=donation,
        ngo=request.user
    ).first()

    if existing_request:

        return redirect('my_requests')

    FoodRequest.objects.create(
        donation=donation,
        ngo=request.user
    )

    donation.status = 'REQUESTED'

    donation.save()

    return redirect('available_food')


# =========================================================
# NGO - MY REQUESTS
# =========================================================

@login_required
@role_required(['NGO'])
def my_requests(request):

    requests = FoodRequest.objects.filter(
        ngo=request.user
    ).order_by('-requested_at')

    return render(
        request,
        'donations/my_requests.html',
        {'requests': requests}
    )


# =========================================================
# VOLUNTEER - PICKUP TASKS
# =========================================================

@login_required
@role_required(['VOLUNTEER'])
def pickup_tasks(request):

    tasks = FoodRequest.objects.filter(
        status='APPROVED'
    ).order_by('-requested_at')

    return render(
        request,
        'donations/pickup_tasks.html',
        {'tasks': tasks}
    )


# =========================================================
# VOLUNTEER - PICKUP HISTORY
# =========================================================

@login_required
@role_required(['VOLUNTEER'])
def pickup_history(request):

    history = FoodRequest.objects.filter(
        status='COLLECTED'
    ).order_by('-requested_at')

    return render(
        request,
        'donations/pickup_history.html',
        {'history': history}
    )


# =========================================================
# VOLUNTEER - MARK FOOD AS COLLECTED
# =========================================================

@login_required
@role_required(['VOLUNTEER'])
def mark_collected(request, request_id):

    food_request = FoodRequest.objects.get(
        id=request_id
    )

    food_request.status = 'COLLECTED'

    food_request.save()

    food_request.donation.status = 'COLLECTED'

    food_request.donation.save()

    return redirect('pickup_tasks')