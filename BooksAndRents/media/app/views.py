import json
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
from django.views.decorators.csrf import csrf_exempt
import os
import requests
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.timezone import now, timedelta


# Create your views here.

def index(request):
        return render(request, 'index.html')

def Promociones(request):
        return render(request, 'Promociones.html')

def Suscripciones(request):
    return render(request, 'Suscripciones.html')

@login_required
def Perfil(request):
    usuario = request.user
    compras = Compra.objects.filter(cliente=usuario)
    suscripcion = Sub.objects.filter(id_us=usuario, invalida=False).first()
    return render(request, 'Perfil.html', {'usuario': usuario, 'compras': compras, 'suscripcion': suscripcion})

@login_required
def Arriendos(request):
    # Verificar si el usuario tiene una suscripción activa
    suscripcion_activa = Sub.objects.filter(id_us=request.user, fecha_inicio__lte=timezone.now(), fecha_inicio__gte=timezone.now()-timedelta(days=30)).exists()

    if not suscripcion_activa:
        messages.error(request, 'Debe tener una suscripción activa para realizar un arriendo.')
        return redirect('Suscripciones')  # Redirige a la página de suscripciones si no está suscrito

    # Obtener los libros con stock disponible
    libros = LibroArr.objects.filter(stock__gt=0)

    if request.method == 'POST':
        # Obtener los libros seleccionados
        libros_ids = request.POST.getlist('libros_ids')  # IDs de los libros seleccionados
        cantidades = request.POST.getlist('cantidades')  # Cantidades de cada libro

        if libros_ids:
            # Crear el arriendo con la fecha de inicio y fin
            nuevo_arriendo = Arriendo(cliente=request.user)
            nuevo_arriendo.save()

            # Crear los ítems de arriendo asociados
            for i, libro_id in enumerate(libros_ids):
                libro = LibroArr.objects.get(id=libro_id)
                cantidad = int(cantidades[i])

                if cantidad > libro.stock:
                    messages.error(request, f'No hay suficiente stock para {libro.nom_libro}.')
                    return redirect('ver_libros_arriendo')

                # Crear un nuevo ítem de arriendo
                ItemArriendo.objects.create(
                    arriendo=nuevo_arriendo,
                    libro=libro,
                    cantidad=cantidad
                )

                # Reducir el stock del libro
                libro.stock -= cantidad
                libro.save()

            messages.success(request, 'Arriendo creado exitosamente.')
            return redirect('Perfil')  # Redirigir al listado de arriendos o página de confirmación

        else:
            messages.error(request, 'Debe seleccionar al menos un libro para arrendar.')

    return render(request, 'Arriendos.html', {'libros': libros})

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

    return redirect('ComprarLibros')

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
    usuario = request.user

    # Verificar si el tipo de suscripción existe
    tipo_sub = get_object_or_404(TipoSubcripscion, id=tipo_sub_id)

    # Verificar si el usuario ya tiene una suscripción activa
    suscripcion_existente = Sub.objects.filter(id_us=usuario).order_by('-fecha_inicio').first()
    if suscripcion_existente and suscripcion_existente.activa:
        messages.error(request, "Ya tienes una suscripción activa.")
        return redirect('Arriendos')  # Cambiar por tu URL de suscripciones

    # Crear nueva suscripción
    nueva_suscripcion = Sub.objects.create(
        id_us=usuario,
        id_ts=tipo_sub,
        fecha_inicio=now().date(),
    )

    messages.success(request, f"Suscripción '{tipo_sub.nombre}' creada exitosamente. ¡Disfrútala!")
    return redirect('Arriendos')  # Cambiar por tu URL de suscripciones

# Confirmación del pago y creación de la suscripción
@login_required
def confirmar_suscripcion(request, tipo_sub_id):
    tipo_sub = get_object_or_404(TipoSubcripscion, id=tipo_sub_id)
    usuario = request.user

    # Verifica nuevamente si el usuario ya tiene una suscripción activa
    suscripcion_existente = Sub.objects.filter(id_us=usuario).order_by('-fecha_inicio').first()
    if suscripcion_existente and suscripcion_existente.activa:
        messages.error(request, "Ya tienes una suscripción activa.")
        return redirect('Arriendos')

    # Crea la suscripción si el pago fue exitoso
    Sub.objects.create(
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
                "currency_id": "CLP"  # moneda local
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
            # Guardar los items en el historial de compras antes de eliminarlos del carrito
            for item in items:
                Compra.objects.create(
                    cliente=request.user,
                    producto=item.producto,
                    cantidad=item.cantidad
                )

            # Eliminar los items del carrito
            items.delete()

            return JsonResponse({"preference_id": preference["id"]})
        else:
            return JsonResponse({"error": "No se pudo crear la preferencia de pago"}, status=500)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)








@login_required
def payment_page(request):
    return render(request, 'payment.html')  #  'payment.html'

def ComprarLibros(request):
    # Obtenemos el término de búsqueda de los GET parameters
    query = request.GET.get('search', '')  # Este es el campo que se pasa en la URL
    if query:
        libros = Libro.objects.filter(nom_libro__icontains=query)  # Filtramos los libros por el nombre
    else:
        libros = Libro.objects.all()  # Si no hay término de búsqueda, mostramos todos los libros

    return render(request, 'ComprarLibros.html', {'libros': libros, 'query': query})

def descargar_imagen_libro(libro):
    """
    Descarga la imagen del libro desde la URL proporcionada en el campo `imagen` y la almacena
    en la ruta especificada en `media/libros`.
    """
    if libro.imagen:
        url = libro.imagen_url  # Usa la URL completa desde el método imagen_url
        ruta_destino = os.path.join(settings.BASE_DIR, "media/libros", f"{libro.id}_imagen.jpg")

        # Crea el directorio si no existe
        os.makedirs(os.path.dirname(ruta_destino), exist_ok=True)

        response = requests.get(url, stream=True)
        if response.status_code == 200:
            with open(ruta_destino, "wb") as file:
                for chunk in response.iter_content(1024):
                    file.write(chunk)
            print(f"Imagen descargada y guardada en {ruta_destino}")
            return ruta_destino
        else:
            print("Error al descargar la imagen.")
    return None

@login_required
def editar_perfil(request):
    usuario = request.user
    if request.method == 'POST':
        usuario.first_name = request.POST.get('first_name')
        usuario.last_name = request.POST.get('last_name')
        usuario.direccion = request.POST.get('direccion')
        usuario.telefono = request.POST.get('telefono')
        usuario.fechanac = request.POST.get('fechanac')
        usuario.genero = request.POST.get('genero')
        usuario.save()
        messages.success(request, 'Datos actualizados correctamente.')
        return redirect('Perfil')  # Redirigir al perfil después de guardar los cambios
    return redirect('Perfil')  # Redirigir si no es POST