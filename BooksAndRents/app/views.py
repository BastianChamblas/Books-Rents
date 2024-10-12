from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse_lazy
from django.views import View
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import mercadopago
from django.http import JsonResponse
# Create your views here.

def index(request):
        return render(request, 'index.html')

def Promociones(request):
        return render(request, 'Promociones.html')

def Suscripciones(request):
    return render(request, 'Suscripciones.html')

def Perfil(request):
    return render(request, 'Perfil.html')

def ComprarLibros(request):
    libros = Libro.objects.all()
    return render(request, 'ComprarLibros.html', {'libros': libros})

def Arriendos(request):
    return render(request, 'Arriendos.html')

def CarritoPagina(request):
    return render(request, 'Carrito.html')

def Patron(request):
    return render(request, 'patron.html')

class RegisterView(View):
    def get(self, request):
        form = CustomUserCreationForm()
        return render(request, 'registration/registro.html', {'form': form})

    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
        return render(request, 'registration/registro.html', {'form': form})

class LoginView(View):
    def get(self, request):
        form = CustomAuthenticationForm()
        return render(request, 'registration/login.html', {'form': form})

    def post(self, request):
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
        return render(request, 'registration/login.html', {'form': form})


@login_required
def agregar_al_carrito(request, libro_id):
    usuario = request.user
    libro = get_object_or_404(Libro, id=libro_id)
    
    cantidad = int(request.POST.get('cantidad', 1))

    if cantidad > libro.stock:
        messages.error(request, 'La cantidad solicitada supera el stock disponible.')
        return redirect('ComprarLibros')
    
    carrito, creado = Carrito.objects.get_or_create(cliente=usuario)

    item_carrito, creado = ItemCarrito.objects.get_or_create(carrito=carrito, producto=libro)

    if not creado:
        item_carrito.cantidad += cantidad
    else:
        item_carrito.cantidad = cantidad

    item_carrito.save()

    libro.restar_stock(cantidad)

    messages.success(request, f'Se han agregado {cantidad} unidad(es) de "{libro.nom_libro}" al carrito.')

    return redirect('ver_carrito')

@login_required
def ver_carrito(request):
    carrito = Carrito.objects.filter(cliente=request.user).first()
    items = carrito.itemcarrito_set.all() if carrito else []
    total = carrito.get_cart_total if carrito else 0

    return render(request, 'carrito.html', {'carrito': carrito, 'items': items, 'total': total})

@login_required
def eliminar_del_carrito(request, item_id):
    item = get_object_or_404(ItemCarrito, id=item_id, carrito__cliente=request.user)
    
    cantidad_a_eliminar = int(request.POST.get('cantidad', 0))
    
    if cantidad_a_eliminar <= 0 or cantidad_a_eliminar > item.cantidad:
        messages.error(request, 'Cantidad inválida.')
        return redirect('ver_carrito')
    
    item.producto.stock += cantidad_a_eliminar
    item.producto.save()

    if item.cantidad > cantidad_a_eliminar:
        item.cantidad -= cantidad_a_eliminar
        item.save()
        messages.success(request, f'Se han eliminado {cantidad_a_eliminar} unidad(es) de "{item.producto.nom_libro}".')
    else:
        item.delete()
        messages.success(request, f'"{item.producto.nom_libro}" ha sido eliminado del carrito.')
    
    return redirect('ver_carrito')

@login_required
def crear_suscripcion(request, tipo_sub_id):
    tipo_sub = TipoSubcripscion.objects.get(id=tipo_sub_id)
    usuario = request.user

    suscripcion_existente = Sub.objects.filter(id_us=usuario).order_by('-fecha_inicio').first()

    if suscripcion_existente and suscripcion_existente.activa:
        messages.error(request, "Ya tienes una suscripción activa.")
        return redirect('Arriendos')

    nueva_suscripcion = Sub.objects.create(
        id_us=usuario,
        id_ts=tipo_sub,
        fecha_inicio=timezone.now()
    )

    messages.success(request, "Suscripción creada exitosamente.")
    return redirect('Arriendos')

# Mercado pago --
@login_required
def checkout(request):
    # Se inicializa Mercado Pago con las credenciales (el access token del test)
    sdk = mercadopago.SDK("APP_USR-3082655413328000-100903-98c8f5f871981af0ee732b102a1e77c0-2028530668")

    # Obtiene el carrito del usuario
    carrito = Carrito.objects.filter(cliente=request.user).first()
    if not carrito:
        return JsonResponse({"error": "No hay artículos en el carrito."}, status=400)

    items = carrito.itemcarrito_set.all()

    # Construir los datos usando lo del carrito
    preference_data = {
        "items": [
            {
                "title": item.producto.nom_libro,
                "quantity": item.cantidad,
                "unit_price": float(item.producto.precio),
                "currency_id": "CLP"  #  moneda local
            } for item in items
        ],
        "payer": {
            "email": request.user.email
        }
    }

    # Crear la preferencia en Mercado Pago con manejo de errores
    try:
        preference_response = sdk.preference().create(preference_data)
        preference = preference_response.get("response", {})

        # Verificar si el preference_id está presente en la respuesta
        if "id" in preference:
            return JsonResponse({"preference_id": preference["id"]})
        else:
            return JsonResponse({"error": "No se pudo crear la preferencia de pago"}, status=500)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@login_required
def payment_page(request):
    return render(request, 'payment.html')  #  'payment.html'