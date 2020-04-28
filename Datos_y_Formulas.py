def porcentaje_de_iva_segun(letra):
    switcher = {
                'A': 10.05,
                'B': 21,
                'C': 70
    }
    return switcher.get(letra, 0)


def precio_neto(precio_unitario, cantidad):
    return precio_unitario * cantidad


def monto_iva(precio_neto, porcentaje_de_iva):
    return precio_neto * porcentaje_de_iva / 100


def precio_venta(precio_neto, monto_iva):
    return precio_neto + monto_iva
