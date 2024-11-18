import re


def validar_rut(rut):
    rut = rut.replace(".", "").replace("-", "").upper()
    if not re.match(r'^\d{7,8}[0-9K]$', rut):
        return False

    cuerpo = rut[:-1]
    dv = rut[-1]

    suma = 0
    multiplicador = 2

    for digito in reversed(cuerpo):
        suma += int(digito) * multiplicador
        multiplicador = 9 if multiplicador == 7 else multiplicador + 1

    resto = suma % 11
    dv_calculado = 'K' if resto == 10 else str(11 - resto)

    return dv == dv_calculado