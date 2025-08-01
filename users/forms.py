from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserRegisterForm(UserCreationForm):
    """
    A custom user registration form that includes an email field.
    """
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']
