from django import forms
from django.contrib.auth.models import User
from .models import UserProfile


class RegistrationForm(forms.Form):

    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Enter username'
            }
        )
    )

    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                'placeholder': 'Enter email address'
            }
        )
    )

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Create password'
            }
        )
    )

    phone = forms.CharField(
        max_length=15,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Enter phone number'
            }
        )
    )

    address = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'placeholder': 'Enter your address',
                'rows': 3
            }
        )
    )

    role = forms.ChoiceField(
        choices=UserProfile.ROLE_CHOICES
    )

    def clean_username(self):

        username = self.cleaned_data['username']

        if User.objects.filter(
            username=username
        ).exists():

            raise forms.ValidationError(
                'Username already exists.'
            )

        return username

    def save(self):

        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password']
        )

        UserProfile.objects.create(
            user=user,
            role=self.cleaned_data['role'],
            phone=self.cleaned_data['phone'],
            address=self.cleaned_data['address']
        )

        return user