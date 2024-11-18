"""
URL configuration for BooksandRents project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app import views
from django.conf import settings
from django.conf.urls.static import static
from app.views import *
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.index, name='index'),
    path('Promociones', views.Promociones , name='Promociones'),
    path('Suscripciones', views.Suscripciones, name='Suscripciones'),
    path('Perfil', views.Perfil, name='Perfil'),
    path('ComprarLibros', views.ComprarLibros, name='ComprarLibros'),
    path('Arriendos', views.Arriendos, name='Arriendos'),
    path('Carrito', views.CarritoPagina, name='Carrito'),
    path('Patron', views.Patron, name='Patron'),
    path('registro', RegisterView.as_view(), name='registro'),
    path('ingreso', LoginView.as_view(), name='ingreso'),
    path('ver_carrito', views.ver_carrito, name='ver_carrito'),
    path('carrito/agregar/<int:libro_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('carrito/eliminar/<int:item_id>/', views.eliminar_del_carrito, name='eliminar_del_carrito'),
    path('crear-suscripcion/<int:tipo_sub_id>/', views.crear_suscripcion, name='crear_suscripcion'),
    path('checkout/', views.checkout, name='checkout'),
    path('payment/', views.payment_page, name='payment_page'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('procesar-pago/', views.procesar_pago, name='procesar_pago'),
    path("confirmacion-pago/", views.confirmacion_pago, name="confirmacion_pago"),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

