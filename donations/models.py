from django.db import models
from django.contrib.auth.models import User


class FoodDonation(models.Model):

    FOOD_TYPE_CHOICES = (
        ('COOKED', 'Cooked Food'),
        ('PACKAGED', 'Packaged Food'),
        ('GROCERY', 'Grocery'),
        ('OTHER', 'Other'),
    )

    STATUS_CHOICES = (
        ('AVAILABLE', 'Available'),
        ('REQUESTED', 'Requested'),
        ('COLLECTED', 'Collected'),
        ('EXPIRED', 'Expired'),
    )

    PRIORITY_CHOICES = (
        ('HIGH', 'High'),
        ('MEDIUM', 'Medium'),
        ('LOW', 'Low'),
    )

    donor = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    food_name = models.CharField(
        max_length=200
    )

    food_type = models.CharField(
        max_length=20,
        choices=FOOD_TYPE_CHOICES
    )

    quantity = models.FloatField()

    preparation_date = models.DateField()

    expiry_date = models.DateField()

    pickup_address = models.TextField()

    distance_km = models.FloatField(
    default=5
)

    description = models.TextField(
        blank=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='AVAILABLE'
    )

    priority = models.CharField(
        max_length=10,
        choices=PRIORITY_CHOICES,
        default='MEDIUM'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.food_name


class FoodRequest(models.Model):

    donation = models.ForeignKey(
        FoodDonation,
        on_delete=models.CASCADE
    )

    ngo = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    requested_at = models.DateTimeField(
        auto_now_add=True
    )

    status = models.CharField(
        max_length=20,
        choices=(
            ('REQUESTED', 'Requested'),
            ('APPROVED', 'Approved'),
            ('REJECTED', 'Rejected'),
            ('COLLECTED', 'Collected'),
        ),
        default='REQUESTED'
    )

    def __str__(self):
        return f"{self.ngo.username} - {self.donation.food_name}"