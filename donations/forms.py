from django import forms
from .models import FoodDonation


class FoodDonationForm(forms.ModelForm):

    class Meta:

        model = FoodDonation

        fields = [
            'food_name',
            'food_type',
            'quantity',
            'preparation_date',
            'expiry_date',
            'pickup_address',
            'distance_km',
            'description'
        ]

        widgets = {

            'preparation_date': forms.DateInput(
                attrs={
                    'type': 'date'
                }
            ),

            'expiry_date': forms.DateInput(
                attrs={
                    'type': 'date'
                }
            ),

            'distance_km': forms.NumberInput(
                attrs={
                    'step': '0.1',
                    'min': '0',
                    'placeholder': 'Enter approximate distance in km'
                }
            ),

            'description': forms.Textarea(
                attrs={
                    'rows': 4,
                    'placeholder': 'Enter additional information about the food'
                }
            ),

            'pickup_address': forms.Textarea(
                attrs={
                    'rows': 3,
                    'placeholder': 'Enter food pickup address'
                }
            ),
        }


    def clean(self):

        cleaned_data = super().clean()

        quantity = cleaned_data.get('quantity')
        distance = cleaned_data.get('distance_km')
        preparation_date = cleaned_data.get('preparation_date')
        expiry_date = cleaned_data.get('expiry_date')

        # Quantity validation
        if quantity is not None and quantity <= 0:

            self.add_error(
                'quantity',
                'Quantity must be greater than 0.'
            )

        # Distance validation
        if distance is not None and distance < 0:

            self.add_error(
                'distance_km',
                'Distance cannot be negative.'
            )

        # Date validation
        if preparation_date and expiry_date:

            if expiry_date < preparation_date:

                self.add_error(
                    'expiry_date',
                    'Expiry date cannot be before preparation date.'
                )

        return cleaned_data