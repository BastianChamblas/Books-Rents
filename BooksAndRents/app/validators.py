import re
from itertools import cycle
from django.core.exceptions import ValidationError

def digito_verificador(rut):
    reversed_digits = map(int, reversed(str(rut)))
    factors = cycle(range(2, 8))
    s = sum(d * f for d, f in zip(reversed_digits, factors))
    return 'K' if (-s) % 11 == 10 else str((-s) % 11)

def validar_rut(value):
    # Limpiar el RUT eliminando puntos, guiones y espacios
    rut = re.sub(r'[^\w]', '', value).upper()

    # Validar que el RUT tenga entre 8 y 9 caracteres
    if not re.match(r'^\d{7,8}[0-9K]$', rut):
        raise ValidationError("El RUT debe tener un formato válido. Ejemplo: 12345678K o 12.345.678-K.")

    # Separar cuerpo y dígito verificador
    cuerpo, dv_ingresado = rut[:-1], rut[-1]

    # Calcular el dígito verificador esperado
    dv_calculado = digito_verificador(cuerpo)

    # Comparar el dígito verificador calculado con el ingresado
    if dv_calculado != dv_ingresado:
        raise ValidationError("El RUT ingresado no es válido.")