from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from .models import Carrito, Usercarrito

@receiver(user_logged_in)
def crear_carrito_al_login(sender, user, request, **kwargs):
    # Verificar si el usuario tiene un carrito asociado
    if not Usercarrito.objects.filter(userc=user).exists():
        # Crear un carrito para el usuario
        user_carrito = Usercarrito.objects.create(userc=user)
        Carrito.objects.create(cliente=user_carrito)
        print(f"Carrito creado para el usuario {user.email}")
    else:
        print(f"El usuario {user.email} ya tiene un carrito.")