from django.contrib import admin
from .models import *

# Register your models here.

class LibroAdmin(admin.ModelAdmin):
    list_display=('id', 'nom_libro', 'precio', 'stock', 'id_genero', 'id_autor', 'imagen')

class LibroArrAdmin(admin.ModelAdmin):
    list_display=('id', 'nom_libro', 'stock', 'id_genero', 'id_autor', 'imagen')

class AutorAdmin(admin.ModelAdmin):
    list_display=('id', 'nombre_autor')

class GeneroLibAdmin(admin.ModelAdmin):
    list_display=('id', 'nombre')

class SubscripcionAdmin(admin.ModelAdmin):
    list_display=('id', 'nom_sus', 'dcto') 

class CustomUserAdmin(admin.ModelAdmin):
    list_display=('id', 'email', 'rut', 'first_name', 'last_name', 'telefono', 'telefono', 'fechanac', 'direccion')

class TipoSubcripcionAdmin(admin.ModelAdmin):
    list_display=('nombre', 'precio', 'dcto')

class SubAdmin(admin.ModelAdmin):
    list_display=('id_us', 'id_ts', 'fecha_inicio')

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Libro, LibroAdmin)
admin.site.register(LibroArr, LibroArrAdmin)
admin.site.register(Autor,AutorAdmin)
admin.site.register(GeneroLib, GeneroLibAdmin)
admin.site.register(Subscripcion, SubscripcionAdmin)
admin.site.register(TipoSubcripscion, TipoSubcripcionAdmin)
admin.site.register(Sub, SubAdmin)