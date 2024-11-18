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
from .utils import *
from django.db import transaction



# Create your views here.

def index(request):
    # Obtenemos los libros en existencia (stock > 0)
    libros = Libro.objects.filter(stock__gt=0)
    return render(request, 'index.html', {'libros': libros})

def Promociones(request):
        return render(request, 'Promociones.html')

def Suscripciones(request):
    return render(request, 'Suscripciones.html')

@login_required
def Arriendos(request):
    # Verificar si el usuario tiene una suscripción activa
    suscripcion_activa = Sub.objects.filter(
        id_us=request.user,
        fecha_inicio__lte=timezone.now(),
        fecha_inicio__gte=timezone.now() - timedelta(days=30),
        invalida=False  # Verifica que la suscripción no esté inválida
    ).exists()

    if not suscripcion_activa:
        messages.error(request, 'Debe tener una suscripción activa para realizar un arriendo.')
        return redirect('Suscripciones')  # Redirige a la página de suscripciones si no está suscrito

    # Obtener los libros con stock disponible para el arriendo
    libros = LibroArr.objects.filter(stock__gt=0)

    # Verifica y descarga las imágenes
    for libro in libros:
        ruta_imagen = os.path.join(settings.MEDIA_ROOT, "librosarr", f"{libro.id}_imagen.jpg")
        if not os.path.exists(ruta_imagen):
            descargar_imagen_libroarr(libro)

    if request.method == 'POST':
        libro_id = request.POST.get('libro_id')
        cantidad = int(request.POST.get('cantidad', 1))

        if libro_id:
            # Verificar que el libro existe
            try:
                libro = LibroArr.objects.get(id=libro_id)
            except LibroArr.DoesNotExist:
                messages.error(request, 'El libro seleccionado no existe.')
                return redirect('Arriendos')

            # Verificar que haya suficiente stock
            if cantidad > libro.stock:
                messages.error(request, f'No hay suficiente stock para {libro.nom_libro}.')
                return redirect('Arriendos')

            # Crear el arriendo para el libro seleccionado
            nuevo_arriendo = Arriendo.objects.create(
                cliente=request.user,  # Asociar al usuario
                producto=libro,  # Asociar al libro
                fecha_inicio=timezone.now(),  # Fecha de inicio actual
            )

            # Establecer la fecha de fin (30 días después de la fecha de inicio)
            nuevo_arriendo.fecha_fin = nuevo_arriendo.fecha_inicio + timedelta(days=30)
            nuevo_arriendo.save()

            # Reducir el stock del libro arrendado
            libro.stock -= cantidad
            libro.save()

            messages.success(request, f'Arriendo de {libro.nom_libro} creado exitosamente.')
            return redirect('Perfil')  # Redirigir al perfil del usuario

        else:
            messages.error(request, 'Debe seleccionar un libro para arrendar.')

    # Obtener los arriendos activos del usuario (donde la fecha de fin no haya pasado)
    arriendos = Arriendo.objects.filter(cliente=request.user, fecha_fin__gte=timezone.now())

    return render(request, 'Arriendos.html', {
        'libros': libros,
        'arriendos': arriendos
    })

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
    # Obtén el carrito del usuario
    carrito = Carrito.objects.filter(cliente=request.user).first()
    items = carrito.itemcarrito_set.all() if carrito else []
    total = carrito.get_cart_total if carrito else 0

    # Verifica si el usuario tiene una suscripción activa
    suscripcion = Sub.objects.filter(id_us=request.user, invalida=False).first()
    descuento = 0
    if suscripcion and suscripcion.activa:
        # Calcula el descuento basado en el porcentaje de la suscripción
        descuento = (total * suscripcion.id_ts.dcto) / 100
        total -= descuento

    return render(request, 'carrito.html', {
        'carrito': carrito,
        'items': items,
        'total': total,
        'descuento': descuento,
        'suscripcion': suscripcion
    })


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


@login_required
def checkout(request):
    sdk = mercadopago.SDK("APP_USR-3082655413328000-100903-98c8f5f871981af0ee732b102a1e77c0-2028530668")

    carrito = Carrito.objects.filter(cliente=request.user).first()
    if not carrito:
        return JsonResponse({"error": "No hay artículos en el carrito."}, status=400)

    items = carrito.itemcarrito_set.all()

    # Calcula el total del carrito
    total = carrito.get_cart_total  # Total sin descuento

    # Verifica si el usuario tiene una suscripción activa
    suscripcion = Sub.objects.filter(id_us=request.user, invalida=False).first()
    descuento = 0
    if suscripcion and suscripcion.activa:
        # Calcula el descuento basado en el porcentaje de la suscripción
        descuento = (total * suscripcion.id_ts.dcto) / 100
        total -= descuento  # Aplica el descuento al total

    # Prepara los datos para la preferencia de Mercado Pago
    preference_data = {
        "items": [
            {
                "title": item.producto.nom_libro,
                "quantity": item.cantidad,
                "unit_price": float(item.producto.precio),
                "currency_id": "CLP"
            } for item in items
        ],
        "payer": {
            "email": request.user.email
        },
        "back_urls": {
            "success": "http://localhost:8000/confirmacion-pago/",
            "failure": "http://localhost:8000/error-pago/",
            "pending": "http://localhost:8000/pago-pendiente/"
        },
        "auto_return": "approved",
        "additional_info": f"Descuento aplicado: {descuento}",  # Información adicional (opcional)
        "amount": total  # El total con descuento
    }

    try:
        # Crear la preferencia de pago en MercadoPago
        preference_response = sdk.preference().create(preference_data)
        preference = preference_response.get("response", {})

        if "id" in preference:
            return JsonResponse({
                "preference_id": preference["id"],
                "init_point": preference["init_point"],
                "total": total,  # El total con descuento
                "descuento": descuento  # El descuento aplicado
            })
        else:
            return JsonResponse({"error": "No se pudo crear la preferencia de pago"}, status=500)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


    
@login_required
def confirmacion_pago(request):
    sdk = mercadopago.SDK("APP_USR-3082655413328000-100903-98c8f5f871981af0ee732b102a1e77c0-2028530668")
    payment_id = request.GET.get("payment_id")
    status = request.GET.get("status")

    if status != "approved" or not payment_id:
        # Si el pago no está aprobado, redirige al usuario a una página de error o muestra un mensaje.
        return render(request, "error_pago.html")

    # Verifica el estado del pago con Mercado Pago
    payment_info = sdk.payment().get(payment_id)
    payment = payment_info.get("response")

    if payment and payment.get("status") == "approved":
        # Obtiene el carrito del usuario
        carrito = Carrito.objects.filter(cliente=request.user).first()
        if carrito:
            items = carrito.itemcarrito_set.all()

            # Registrar cada producto comprado en la tabla Compra
            for item in items:
                Compra.objects.create(
                    cliente=carrito.cliente,
                    producto=item.producto,
                    cantidad=item.cantidad
                )

            # Vacía el carrito después de registrar la compra
            items.delete()

        # Redirige a una página de confirmación de compra o muestra un mensaje de éxito
        return render(request, "confirmacion_exito.html")
    else:
        # Si el pago no está aprobado, redirige al usuario a una página de error
        return render(request, "error_pago.html")

@csrf_exempt
def pago_webhook(request):
    if request.method == "POST":
        sdk = mercadopago.SDK("APP_USR-3082655413328000-100903-98c8f5f871981af0ee732b102a1e77c0-2028530668")

        # Parsear la información de la notificación
        payment_data = json.loads(request.body.decode('utf-8'))
        payment_id = payment_data.get("data", {}).get("id")
        
        if not payment_id:
            return JsonResponse({"error": "Falta el ID del pago"}, status=400)

        # Obtiene los detalles del pago para verificar el estado
        payment_info = sdk.payment().get(payment_id)
        payment = payment_info.get("response")

        if payment and payment.get("status") == "approved":
            user_email = payment["payer"]["email"]

            # Busca al cliente en función de su email
            carrito = Carrito.objects.filter(cliente__email=user_email).first()
            if carrito:
                items = carrito.itemcarrito_set.all()

                # Registrar cada producto comprado en la tabla Compra
                for item in items:
                    Compra.objects.create(
                        cliente=carrito.cliente,
                        producto=item.producto,
                        cantidad=item.cantidad
                    )

                # Vacía el carrito después de registrar la compra
                items.delete()

            return JsonResponse({"status": "Compra registrada y carrito vaciado"})
        else:
            return JsonResponse({"error": "El pago no fue aprobado"}, status=400)
    else:
        return JsonResponse({"error": "Método no permitido"}, status=405)


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
        ruta_destino = os.path.join(settings.BASE_DIR, "media/librosarr", f"{libro.id}_imagen.jpg")

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

def descargar_imagen_libroarr(libroarr):
    """
    Descarga la imagen del libro desde la URL proporcionada en el campo `imagen` del modelo `LibroArr`
    y la almacena en la carpeta `media/librosarr`.
    """
    if libroarr.imagen:
        # Define la ruta destino
        ruta_destino = os.path.join(settings.MEDIA_ROOT, "librosarr", f"{libroarr.id}_imagen.jpg")

        # Crea el directorio si no existe
        os.makedirs(os.path.dirname(ruta_destino), exist_ok=True)

        try:
            # Realiza la solicitud para descargar la imagen
            response = requests.get(libroarr.imagen, stream=True)
            if response.status_code == 200:
                with open(ruta_destino, "wb") as file:
                    for chunk in response.iter_content(1024):
                        file.write(chunk)
                print(f"Imagen descargada y guardada en {ruta_destino}")
                return ruta_destino
            else:
                print(f"Error al descargar la imagen. Código de estado: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Error en la solicitud de descarga: {e}")
    else:
        print("No se proporcionó una URL válida para la imagen.")
    return None




import re
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Compra, Sub

def validar_rut(rut: str) -> bool:
    # Limpiar el RUT
    rut = rut.replace(".", "").replace("-", "").upper()

    # Verifica que el RUT tenga al menos 2 caracteres
    if len(rut) < 2:
        return False
    
    # Paso 2: Separar el cuerpo y el dígito verificador
    cuerpo = rut[:-1]
    dv_ingresado = rut[-1]

    # Paso 3: Calcular el dígito verificador esperado
    factores = [2, 3, 4, 5, 6, 7, 2, 3, 4, 5, 6, 7]  # Factor para los RUTs chilenos
    suma = 0
    for i, digito in enumerate(reversed(cuerpo)):
        suma += int(digito) * factores[i % len(factores)]
    
    resto = suma % 11
    dv_calculado = str(11 - resto) if resto != 0 else '0'
    if dv_calculado == '10':
        dv_calculado = 'K'
    
    # Paso 4: Comparar el dígito verificador calculado con el ingresado
    return dv_calculado == dv_ingresado

# Prueba de la función con un RUT válido
print(validar_rut("12.345.678-5"))  # Esto debería devolver True

@login_required
def Perfil(request):
    usuario = request.user
    compras = Compra.objects.filter(cliente=usuario)
    suscripcion = Sub.objects.filter(id_us=usuario, invalida=False).first()

    if request.method == 'POST':
        # Manejo de edición de perfil
        errors = {}

        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        direccion = request.POST.get('direccion', '').strip()
        telefono = request.POST.get('telefono', '').strip()
        fechanac = request.POST.get('fechanac', '').strip()
        rut = request.POST.get('rut', '').strip()

        # Validaciones básicas
        if not first_name:
            errors['first_name'] = 'El nombre no puede estar vacío.'
        if not last_name:
            errors['last_name'] = 'El apellido no puede estar vacío.'
        if not direccion:
            errors['direccion'] = 'La dirección no puede estar vacía.'
        if not telefono:
            errors['telefono'] = 'El teléfono no puede estar vacío.'
        if not fechanac:
            errors['fechanac'] = 'La fecha de nacimiento no puede estar vacía.'
        if not rut:
            errors['rut'] = 'El RUT no puede estar vacío.'
        elif not validar_rut(rut):  # Aquí estamos llamando la función de validación
            errors['rut'] = 'El RUT ingresado no es válido.'

        if errors:
            # Renderizar perfil con errores
            return render(request, 'Perfil.html', {
                'usuario': usuario,
                'compras': compras,
                'suscripcion': suscripcion,
                'errors': errors
            })

        # Guardar los cambios si no hay errores
        usuario.first_name = first_name
        usuario.last_name = last_name
        usuario.direccion = direccion
        usuario.telefono = telefono
        usuario.fechanac = fechanac
        usuario.rut = rut
        usuario.save()
        messages.success(request, 'Datos actualizados correctamente.')
        return redirect('Perfil')

    # Manejo de solicitud GET: Mostrar perfil
    return render(request, 'Perfil.html', {
        'usuario': usuario,
        'compras': compras,
        'suscripcion': suscripcion
    })



from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from .models import TipoSubcripscion, Sub
from .models import CustomUser  # Asegúrate de que este modelo esté correctamente importado
from django.utils.timezone import now
import json

@csrf_exempt
def procesar_pago(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            email = data.get('email')
            tipo = data.get('tipo')

            # Verifica que los datos están presentes
            if not email or not tipo:
                return JsonResponse({'success': False, 'message': 'Faltan datos.'}, status=400)

            # Buscar o crear usuario
            usuario, created = CustomUser.objects.get_or_create(
                email=email,
                defaults={'first_name': 'Nombre', 'last_name': 'Apellido', 'is_active': True}
            )

            # Obtener tipo de suscripción
            tipo_sub = get_object_or_404(TipoSubcripscion, nombre=tipo)

            # Verificar suscripción activa
            suscripcion_existente = Sub.objects.filter(id_us=usuario, invalida=False).first()
            if suscripcion_existente:
                return JsonResponse({'success': False, 'message': 'Ya tienes una suscripción activa.'}, status=400)

            # Crear nueva suscripción
            nueva_suscripcion = Sub.objects.create(
                id_us=usuario,
                id_ts=tipo_sub,
                fecha_inicio=now().date(),
                invalida=False
            )

            print(f"Suscripción creada: {nueva_suscripcion}")  # Depuración

            return JsonResponse({'success': True, 'message': f'Suscripción al plan {tipo} creada exitosamente.'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)

    return JsonResponse({'success': False, 'message': 'Método no permitido.'}, status=405)










