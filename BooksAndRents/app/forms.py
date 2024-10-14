# users/forms.py
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import *
from .models import *

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'rut', 'telefono', 'fechanac', 'direccion')

class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'password']