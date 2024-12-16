# users/forms.py
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import *
from .models import *

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'rut', 'telefono', 'fechanac', 'direccion')
        widgets = {
            'fechanac': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }
        labels = {
            'email': 'Correo Electrónico',
            'first_name': 'Nombre',
            'last_name': 'Apellido',
            'rut': 'RUT',
            'telefono': 'Teléfono',
            'fechanac': 'Fecha de Nacimiento',
            'direccion': 'Dirección',
        }

class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'password']
        labels = {
            'email': 'Correo Electrónico',
            'password': 'Contraseña',
        }