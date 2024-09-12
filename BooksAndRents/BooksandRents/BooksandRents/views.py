from django.http import HttpResponse
from django.shortcuts import render

def index(request):
        return render(request, 'index.html')



def Promociones(request):
        return render(request, 'Promociones.html')

def Suscripciones(request):
    return render(request, 'Suscripciones.html')

def Perfil(request):
    return render(request, 'Perfil.html')

def ComprarLibros(request):
    return render(request, 'ComprarLibros.html')

def Arriendos(request):
    return render(request, 'Arriendos.html')

def Carrito(request):
    return render(request, 'Carrito.html')