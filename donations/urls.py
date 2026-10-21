from django.urls import path
from . import views

urlpatterns = [
    path('donate/', views.donate_food, name='donate_food'),
    path('my-donations/', views.my_donations, name='my_donations'),
    path('available-food/', views.available_food, name='available_food'),

    path(
        'request-food/<int:donation_id>/',
        views.request_food,
        name='request_food'
    ),

    path('my-requests/', views.my_requests, name='my_requests'),

    path(
        'pickup-tasks/',
        views.pickup_tasks,
        name='pickup_tasks'
    ),

    path('pickup-history/', views.pickup_history, name='pickup_history'),

    path(
    'mark-collected/<int:request_id>/',
    views.mark_collected,
    name='mark_collected'
),
]