"""
Authentication and registration forms.
All fields styled with Tailwind utility classes via the 'attrs' dict.
"""

from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import SetPasswordForm
from .models import User

# Shared Tailwind classes for form inputs
INPUT_CLASS = (
    'w-full px-4 py-3 rounded-lg border border-cream-border bg-cream '
    'text-text-primary placeholder-text-muted text-sm '
    'focus:outline-none focus:ring-2 focus:ring-burgundy focus:border-transparent '
    'transition duration-200'
)


class UserRegistrationForm(forms.ModelForm):
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'class': INPUT_CLASS, 'placeholder': 'Create a password'}),
    )
    password2 = forms.CharField(
        label='Confirm password',
        widget=forms.PasswordInput(attrs={'class': INPUT_CLASS, 'placeholder': 'Repeat your password'}),
    )

    class Meta:
        model  = User
        fields = ('first_name', 'last_name', 'email', 'phone_number')
        widgets = {
            'first_name':   forms.TextInput(attrs={'class': INPUT_CLASS, 'placeholder': 'First name'}),
            'last_name':    forms.TextInput(attrs={'class': INPUT_CLASS, 'placeholder': 'Last name'}),
            'email':        forms.EmailInput(attrs={'class': INPUT_CLASS, 'placeholder': 'Email address'}),
            'phone_number': forms.TextInput(attrs={'class': INPUT_CLASS, 'placeholder': 'Phone number (optional)'}),
        }

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('An account with this email already exists.')
        return email

    def clean(self):
        cleaned = super().clean()
        p1 = cleaned.get('password1')
        p2 = cleaned.get('password2')
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError('Passwords do not match.')
        return cleaned

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class UserLoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': INPUT_CLASS, 'placeholder': 'Email address', 'autofocus': True}),
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': INPUT_CLASS, 'placeholder': 'Password'}),
    )

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        self.user   = None
        super().__init__(*args, **kwargs)

    def clean(self):
        email    = self.cleaned_data.get('email', '').lower()
        password = self.cleaned_data.get('password', '')

        if email and password:
            self.user = authenticate(self.request, username=email, password=password)
            if self.user is None:
                raise forms.ValidationError('Invalid email or password. Please try again.')
            if not self.user.is_active:
                raise forms.ValidationError('This account has been deactivated.')
        return self.cleaned_data

    def get_user(self):
        return self.user


class UserProfileForm(forms.ModelForm):
    class Meta:
        model  = User
        fields = ('first_name', 'last_name', 'phone_number', 'address')
        widgets = {
            'first_name':   forms.TextInput(attrs={'class': INPUT_CLASS}),
            'last_name':    forms.TextInput(attrs={'class': INPUT_CLASS}),
            'phone_number': forms.TextInput(attrs={'class': INPUT_CLASS}),
            'address':      forms.Textarea(attrs={'class': INPUT_CLASS, 'rows': 3}),
        }
