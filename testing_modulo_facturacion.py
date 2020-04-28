import modulo_facturacion as MF
import unittest as UT


class TestFacturacion(UT.TestCase):

    def test_tras_facturar_pedido_la_cabecera_es_creada_correctamente(self):
        cliente1 = MF.Cliente(1, 'Pablo Rodriguez', "Calle 100", 'A', "DNI", 10)
        producto1 = MF.Producto(1, "Producto 1", 10)
        producto2 = MF.Producto(2, "Producto 1", 20)
        pedido1 = MF.Pedido(1, cliente1, [(producto1, 1), (producto2, 1)])
        factura = MF.facturar(pedido1)

        self.assertEqual(factura.cabecera.cliente, cliente1)
        self.assertEqual(factura.cabecera.letra, 'A')

        self.assertEqual(factura.cabecera.numero_de_identificacion, MF.factura_number)

    def test_tras_facturar_pedido_el_detalle_contiene_los_precios_correctos(self):
        cliente1 = MF.Cliente(1, 'Pablo Rodriguez', "Calle 100", 'B', "DNI", 10)
        producto1 = MF.Producto(1, "Producto 1", 10)
        pedido1 = MF.Pedido(1, cliente1, [(producto1, 1)])
        factura = MF.facturar(pedido1)

        self.assertEqual(factura.detalle[0].precio_neto, 10)
        self.assertEqual(factura.detalle[0].monto_iva, 2.1)
        self.assertEqual(factura.detalle[0].precio_venta, 12.1)

    def test_tras_facturar_pedido_de_dos_productos_la_factura_contiene_2_lineas_de_detalles(self):
        cliente1 = MF.Cliente(1, 'Pablo Rodriguez', "Calle 100", 'A', "DNI", 10)
        producto1 = MF.Producto(1, "Producto 1", 10)
        producto2 = MF.Producto(2, "Producto 1", 20)
        pedido1 = MF.Pedido(1, cliente1, [(producto1, 1), (producto2, 1)])
        factura = MF.facturar(pedido1)

        self.assertEqual(len(factura.detalle), 2)

    def test_tras_facturar_un_pedido_el_total_y_el_total_iva_son_correctos_en_la_factura(self):
        cliente1 = MF.Cliente(1, 'Pablo Rodriguez', "Calle 100", 'B', "DNI", 10)
        producto1 = MF.Producto(1, "Producto 1", 10)
        producto2 = MF.Producto(2, "Producto 1", 20)
        pedido1 = MF.Pedido(1, cliente1, [(producto1, 1), (producto2, 1)])
        factura = MF.facturar(pedido1)

        self.assertEqual('{0:.2f}'.format(factura.pie.total), '36.30')
        self.assertEqual('{0:.2f}'.format(factura.pie.total_iva), '6.30')

    def test_tras_cancelar_factura_generado_de_nota_credito_con_total_correcto(self):
        cliente1 = MF.Cliente(1, 'Pablo Rodriguez', "Calle 100", 'A', "DNI", 10)
        producto1 = MF.Producto(1, "Producto 1", 10)
        producto2 = MF.Producto(2, "Producto 1", 20)
        pedido1 = MF.Pedido(1, cliente1, [(producto1, 1), (producto2, 1)])
        factura = MF.facturar(pedido1)

        nota_credito = MF.cancelar(factura)

        self.assertEqual(nota_credito.pie.total, factura.pie.total)

    def test_el_reporte_de_operatoria_se_genera_exitosamente(self):
        cliente1 = MF.Cliente(1, 'Pablo Rodriguez', "Calle 100", 'A', "DNI", 10)
        cliente2 = MF.Cliente(2, 'Luis Garcia', "Bleh 200", 'B', "DNI", 20)
        cliente3 = MF.Cliente(3, 'Roberto Gonzalez', "Bleh 300", 'X', "DNI", 30)
        producto1 = MF.Producto(1, "Producto 1", 10)
        producto2 = MF.Producto(2, "Producto 1", 20)
        producto3 = MF.Producto(3, "Producto 1", 30)
        pedido1 = MF.Pedido(1, cliente1, [(producto1, 1), (producto2, 1)])
        pedido2 = MF.Pedido(2, cliente2, [(producto2, 2), (producto3, 2)])
        pedido3 = MF.Pedido(3, cliente3, [(producto1, 3), (producto3, 3)])
        pedido4 = MF.Pedido(4, cliente1, [(producto1, 4), (producto2, 4), (producto3, 4)])

        pedidos = [pedido1, pedido2, pedido3, pedido4]
        factura1 = MF.facturar(pedido1)
        factura2 = MF.facturar(pedido2)
        factura3 = MF.facturar(pedido3)
        factura4 = MF.facturar(pedido4)
        facturas = [factura1, factura2, factura3, factura4]
        cancelaciones = [factura1]

        MF.generacion_de_reporte_para_operatoria(facturas, cancelaciones)

        reporte = open("Reporte de Operatoria", "r")
        linea = reporte.readline()
        reporte.close()
        self.assertEqual(linea, "Pablo Rodriguez-Factura-A-0001-04/28/20-$33.015\n")
