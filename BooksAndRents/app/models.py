from django.db import models
from django.http import JsonResponse
from django.contrib.auth.models import *
from django.shortcuts import get_object_or_404
from django.utils import timezone
from datetime import timedelta
# Create your models here.


class CustomUserManager(BaseUserManager):
    """Manager para el modelo CustomUser"""
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('El usuario debe tener un correo electrónico')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Crea y guarda un superusuario"""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('El superusuario debe tener is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('El superusuario debe tener is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    """Modelo de usuario personalizado donde el email es el identificador único"""
    email = models.EmailField(unique=True)
    rut = models.CharField(max_length=50, null=True, blank=True)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    telefono = models.IntegerField(null=True, blank=True)
    fechanac = models.DateField(null=True, blank=True)
    direccion = models.CharField(max_length=100, null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = CustomUserManager()

    def __str__(self):
        return self.email
    
class Subscripcion(models.Model):
    nom_sus = models.CharField(max_length=100)
    dcto = models.IntegerField()

    def __str__(self):
        return self.nom_sus

class UserSub(models.Model):
    id_Sub = models.ForeignKey(Subscripcion, on_delete=models.CASCADE, null=True, blank=True)
    id_usuario = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)

class GeneroLib(models.Model):
    nombre = models.CharField(max_length=200)

    def __str__(self):
        return self.nombre
    
class Autor(models.Model):
    nombre_autor = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre_autor

class Libro(models.Model):
    nom_libro = models.CharField(max_length=255)
    precio = models.IntegerField()
    stock = models.IntegerField()
    id_genero = models.ForeignKey('GeneroLib', on_delete=models.CASCADE, null=True, blank=True)
    id_autor = models.ForeignKey('Autor', on_delete=models.CASCADE, null=True, blank=True)
    imagen = models.ImageField(upload_to='libros/', null=True)

    def __str__(self):
        return self.nom_libro

    def restar_stock(self, cantidad):
        """Resta una cantidad específica del stock."""
        if self.stock >= cantidad:
            self.stock -= cantidad
            self.save()
    
class LibroArr(models.Model):
    nom_libro = models.CharField(max_length=255)
    stock = models.IntegerField()
    id_genero = models.ForeignKey(GeneroLib, on_delete=models.CASCADE, null=True, blank=True)
    id_autor = models.ForeignKey(Autor, on_delete=models.CASCADE, null=True, blank=True)
    imagen = models.ImageField(upload_to='libros/', null=True)

    def __str__(self):
        return self.nom_libro

class Carrito(models.Model):
    cliente = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    @property
    def get_cart_total(self):
        items = self.itemcarrito_set.all()
        total = sum([item.get_total for item in items])
        return total

    @property
    def get_cart_items(self):
        items = self.itemcarrito_set.all()
        total = sum([item.cantidad for item in items])
        return total

class ItemCarrito(models.Model):
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE)
    producto = models.ForeignKey(Libro, on_delete=models.CASCADE)
    cantidad = models.IntegerField(default=1)

    def __str__(self):
        return self.producto.nom_libro

    @property
    def get_total(self):
        return self.producto.precio * self.cantidad
    
class TipoSubcripscion(models.Model):
    nombre = models.CharField(max_length=255)
    precio = models.IntegerField()
    dcto = models.IntegerField()

    def __str__(self):
        return self.nombre    

class Sub(models.Model):
    id_us = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True)
    id_ts = models.ForeignKey(TipoSubcripscion, on_delete=models.CASCADE, blank=True, null=True)
    fecha_inicio = models.DateField(default=timezone.now)  # Fecha de inicio de la suscripción

    @property
    def fecha_fin(self):
        # Calcula la fecha de fin sumando 30 días a la fecha de inicio
        return self.fecha_inicio + timedelta(days=30)

    @property
    def activa(self):
        # Retorna True si la suscripción aún es válida
        return timezone.now().date() <= self.fecha_fin


class Arriendo(models.Model):
    cliente = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    fecha_inicio = models.DateField(default=timezone.now)
    fecha_fin = models.DateField()

    def save(self, *args, **kwargs):
        if not self.fecha_fin:
            self.fecha_fin = self.fecha_inicio + timedelta(days=30)
        super(Arriendo, self).save(*args, **kwargs)

class ItemArriendo(models.Model):
    arriendo = models.ForeignKey(Arriendo, on_delete=models.CASCADE)
    libro = models.ForeignKey(LibroArr, on_delete=models.CASCADE)
    cantidad = models.IntegerField()

    def __str__(self):
        return f'{self.cantidad} x {self.libro.nom_libro}'