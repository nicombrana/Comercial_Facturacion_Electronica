import concurrent.futures
import datetime
import Datos_y_Formulas as Calculadora


factura_number = 0
nota_credito_number = 0


class Cliente:
    def __init__(
        self,
        numero_cliente,
        nombre,
        domicilio,
        condicion_impositiva,
        tipo_documento,
        numero_documento
    ):
        self.numero_cliente = numero_cliente
        self.nombre = nombre
        self.domicilio = domicilio
        self.condicion_impositiva = condicion_impositiva
        self.tipo_documento = tipo_documento
        self.numero_documento = numero_documento


class Pedido:
    def __init__(self, numero_pedido, cliente, detalles):
        self.numero_pedido = numero_pedido
        self.cliente = cliente
        self.detalles = detalles


class Producto:
    def __init__(self, codigo, nombre, precio):
        self.codigo = codigo
        self.nombre = nombre
        self.precio = precio


class Cabecera:
    def __init__(self, fecha_de_emision, numero_de_identificacion, cliente):
        self.fecha_de_emision = fecha_de_emision
        self.numero_de_identificacion = numero_de_identificacion
        self.codigo_de_emision = '0000'
        self.letra = cliente.condicion_impositiva
        self.cliente = cliente
# numero_de_identificacion puede ser nro de factura o nro de nota de credito


class Factura:
    def __init__(self, cabecera, detalle, pie):
        self.cabecera = cabecera
        self.detalle = detalle
        self.pie = pie


class Detalle:
    def __init__(self, producto, cantidad, porcentaje_de_iva):
        self.producto = producto.nombre
        self.precio_unitario = producto.precio
        self.porcentaje_de_iva = porcentaje_de_iva
        self.cantidad = cantidad
        self.precio_neto = Calculadora.precio_neto(self.precio_unitario, self.cantidad)
        self.monto_iva = Calculadora.monto_iva(self.precio_neto, self.porcentaje_de_iva)
        self.precio_venta = Calculadora.precio_venta(self.precio_neto, self.monto_iva)


class NotaCredito:
    def __init__(self, cabecera, pie):
        self.cabecera = cabecera
        self.pie = pie


class Pie:
    def __init__(self, total):
        self.total = total


class PieFactura(Pie):
    def __init__(self, total, total_iva):
        self.total = total
        self.total_iva = total_iva


def modulo_facturacion_cancelacion_y_generado_de_reporte(pedidos, cancelaciones):
    facturas = realizar_facturacion(pedidos)
    notas_de_credito = realizar_cancelacion_pedidos(cancelaciones, pedidos)
    generacion_de_reporte_para_operatoria(facturas, notas_de_credito)


def realizar_facturacion(pedidos):
    nuevas_facturas = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        for nueva_factura in executor.map(lambda pedido: facturar(pedido), pedidos):
            nuevas_facturas.append(nueva_factura)
    return nuevas_facturas


def facturar(pedido):
    cabecera = generar_cabecera_para(numero_de_factura(), pedido.cliente)
    detalles = escribir_detalles(pedido)
    pie = escribir_pie_factura(detalles)
    factura = Factura(cabecera, detalles, pie)
    return factura


def realizar_cancelacion_pedidos(cancelaciones, pedidos):
    nuevas_notas_credito = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        for nota_credito in executor.map(lambda factura: cancelar(factura), cancelaciones):
            nuevas_notas_credito.append(nota_credito)
            return nuevas_notas_credito


def cancelar(factura):
    cabecera = generar_cabecera_para(numero_nota_credito(), factura.cabecera.cliente)
    pie = Pie(factura.pie.total)
    nota_credito = NotaCredito(cabecera, pie)
    return nota_credito


def generacion_de_reporte_para_operatoria(facturas, notas_de_credito):
    reporte = open('Reporte de Operatoria', "w+")
    for factura in facturas:
        escribir_linea_para(factura, 'Factura', reporte)
    for nota in notas_de_credito:
        escribir_linea_para(nota, 'NotaDeCredito', reporte)
    reporte.close()


def generar_cabecera_para(numero_de_identificacion, cliente):
    fecha_de_emision = datetime.datetime.now().strftime("%x")
    return Cabecera(fecha_de_emision, numero_de_identificacion, cliente)


def escribir_detalles(pedido):
    cliente = pedido.cliente
    detalles = []
    for (producto_comprado, cantidad) in pedido.detalles:
        detalle = generar_detalle_para(producto_comprado, cantidad, cliente)
        detalles.append(detalle)
    return detalles


def generar_detalle_para(producto_comprado, cantidad, cliente):
    porcentaje_iva = Calculadora.porcentaje_de_iva_segun(cliente.condicion_impositiva)
    return Detalle(producto_comprado, cantidad, porcentaje_iva)


def escribir_pie_factura(detalles):
    totales_unitarios = map(lambda detalle: detalle.precio_venta, detalles)
    total = sum(totales_unitarios, 0)
    totales_iva = map(lambda detalle: detalle.monto_iva, detalles)
    total_iva = sum(totales_iva, 0)
    return PieFactura(total, total_iva)


def escribir_linea_para(nota_o_factura, tipo_documento, reporte):
    especificacion = []
    especificacion.append(nota_o_factura.cabecera.cliente.nombre)
    especificacion.append(tipo_documento)
    especificacion.append(nota_o_factura.cabecera.letra)
    especificacion.append(str(nota_o_factura.cabecera.numero_de_identificacion).zfill(4))
    especificacion.append(nota_o_factura.cabecera.fecha_de_emision)
    precio = "$" + str(nota_o_factura.pie.total)
    especificacion.append(precio)
    linea = "-".join(especificacion) + "\n"
    reporte.write(linea)


def numero_de_factura():
    global factura_number
    factura_number += 1
    return factura_number


def numero_nota_credito():
    global nota_credito_number
    nota_credito_number += 1
    return nota_credito_number
