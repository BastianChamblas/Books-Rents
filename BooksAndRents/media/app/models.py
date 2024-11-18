from django.db import models
from django.http import JsonResponse
from django.contrib.auth.models import *
from django.shortcuts import get_object_or_404
from django.utils import timezone
from datetime import timedelta
import os
import requests
import re
from django.conf import settings

from .google_drive_service import get_file_url
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
  # Asegúrate de tener la función ajustada














class Libro(models.Model):
    nom_libro = models.CharField(max_length=255)
    precio = models.IntegerField()
    stock = models.IntegerField()
    id_genero = models.ForeignKey('GeneroLib', on_delete=models.CASCADE, null=True, blank=True)
    id_autor = models.ForeignKey('Autor', on_delete=models.CASCADE, null=True, blank=True)
    imagen = models.CharField(max_length=500, null=True, blank=True)  # Puede almacenar la URL completa o el file_id

    def __str__(self):
        return self.nom_libro

    def restar_stock(self, cantidad):
        if self.stock >= cantidad:
            self.stock -= cantidad
            self.save()
        else:
            raise ValueError("No hay suficiente stock disponible")

    @property
    def imagen_local_path(self):
        """Devuelve la ruta local de la imagen."""
        if self.imagen:
            return os.path.join(settings.MEDIA_ROOT, 'libros', f"{self.id}_imagen.jpg")
        return None

    @property
    def imagen_url(self):
        """Descarga la imagen si no existe localmente y devuelve la URL local."""
        local_path = self.imagen_local_path
        if local_path and not os.path.exists(local_path):
            self.descargar_imagen()
        return f"/media/libros/{self.id}_imagen.jpg" if self.imagen else ""
    
    def descargar_imagen(self):
        """Descarga la imagen desde Google Drive y la guarda localmente."""
        if self.imagen:
            # Extraer el file_id usando una expresión regular
            match = re.search(r'/d/([a-zA-Z0-9_-]+)', self.imagen)
            if match:
                file_id = match.group(1)
                url = f"https://drive.google.com/uc?export=view&id={file_id}&confirm=t"
                print(f"Descargando imagen desde {url}")
                try:
                    response = requests.get(url, stream=True)
                    response.raise_for_status()  # Esto generará una excepción para errores HTTP
                    os.makedirs(os.path.dirname(self.imagen_local_path), exist_ok=True)
                    with open(self.imagen_local_path, "wb") as file:
                        for chunk in response.iter_content(1024):
                            file.write(chunk)
                    print(f"Imagen descargada y almacenada en {self.imagen_local_path}")
                except requests.exceptions.RequestException as e:
                    print(f"Error al descargar la imagen desde {url}: {e}")
            else:
                print("URL de imagen no válida.")


























    
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

    def realizar_pago(self):
        items = self.itemcarrito_set.all()
        for item in items:
            Compra.objects.create(
                cliente=self.cliente,
                producto=item.producto,
                cantidad=item.cantidad
            )
        # Eliminar todos los items del carrito después del pago
        items.delete()

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
    fecha_inicio = models.DateField(default=timezone.now)
    invalida = models.BooleanField(default=False)

    @property
    def fecha_fin(self):
        return self.fecha_inicio + timedelta(days=30)

    @property
    def activa(self):
        return timezone.now().date() <= self.fecha_fin and not self.invalida

    def actualizar_invalida(self):
        tiene_arriendo_atrasado = Arriendo.objects.filter(cliente=self.id_us, arriendo_atraso=True).exists()
        self.invalida = tiene_arriendo_atrasado
        self.save(update_fields=['invalida'])  # Solo actualiza el campo invalida, para evitar recursión

    def save(self, *args, **kwargs):
        # Llamamos a actualizar_invalida solo si realmente se necesita actualizar el campo
        if not self.pk or not self.invalida == self._original_invalida:
            self.actualizar_invalida()
        
        super(Sub, self).save(*args, **kwargs)
        
    def save_initial_invalida(self):
        # Guardamos el valor inicial de 'invalida' para evitar llamadas recursivas
        self._original_invalida = self.invalida

class Arriendo(models.Model):
    cliente = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    fecha_inicio = models.DateField(default=timezone.now)
    fecha_fin = models.DateField()
    arriendo_atraso = models.BooleanField(default=False)
    libro_entregado = models.BooleanField(default=False)
    arrlibro = models.ForeignKey(LibroArr, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        # Calcula la fecha de fin si no ha sido especificada
        if not self.fecha_fin:
            self.fecha_fin = self.fecha_inicio + timedelta(days=30)
        
        # Verifica si el arriendo está en atraso
        if timezone.now().date() > self.fecha_fin and not self.libro_entregado:
            self.arriendo_atraso = True
        else:
            self.arriendo_atraso = False

        super(Arriendo, self).save(*args, **kwargs)

class ItemArriendo(models.Model):
    arriendo = models.ForeignKey(Arriendo, on_delete=models.CASCADE)
    libro = models.ForeignKey(LibroArr, on_delete=models.CASCADE)
    cantidad = models.IntegerField()

    def __str__(self):
        return f'{self.cantidad} x {self.libro.nom_libro}'

class Compra(models.Model):
    cliente = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    producto = models.ForeignKey(Libro, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    fecha_compra = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nom_libro} - {self.fecha_compra}"