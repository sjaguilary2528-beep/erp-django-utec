from decimal import Decimal

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from clientes.models import Cliente
from productos.models import Categoria, Producto
from .models import Venta, DetalleVenta


class VentaPDFTests(TestCase):

    def setUp(self):
        Usuario = get_user_model()

        self.usuario = Usuario.objects.create_user(
            username='usuario_pruebas_pdf',
            password='PruebaSegura123'
        )

        self.cliente = Cliente.objects.create(
            nombre='Cliente de prueba',
            correo='cliente_prueba@example.com'
        )

        self.categoria = Categoria.objects.create(
            nombre='Categoria de prueba'
        )

        self.producto = Producto.objects.create(
            nombre='Producto de prueba',
            precio=Decimal('125.00'),
            stock=10,
            categoria=self.categoria
        )

        self.venta = Venta.objects.create(
            cliente=self.cliente
        )

        DetalleVenta.objects.create(
            venta=self.venta,
            producto=self.producto,
            cantidad=2,
            precio_unitario=Decimal('125.00')
        )

        self.url = reverse(
            'ventas:pdf',
            kwargs={'venta_id': self.venta.pk}
        )

    def autenticar(self):
        self.client.force_login(self.usuario)

    def test_pdf_requiere_autenticacion(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

    def test_pdf_responde_correctamente(self):
        self.autenticar()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_pdf_tiene_content_type_correcto(self):
        self.autenticar()
        response = self.client.get(self.url)
        self.assertEqual(response['Content-Type'], 'application/pdf')

    def test_pdf_contiene_firma_pdf(self):
        self.autenticar()
        response = self.client.get(self.url)
        self.assertTrue(response.content.startswith(b'%PDF'))

    def test_pdf_se_descarga_como_adjunto(self):
        self.autenticar()
        response = self.client.get(self.url)

        self.assertIn('attachment', response['Content-Disposition'])
        self.assertIn(
            f'factura_{self.venta.pk:05d}.pdf',
            response['Content-Disposition']
        )

    def test_pdf_venta_inexistente_devuelve_404(self):
        self.autenticar()

        url = reverse(
            'ventas:pdf',
            kwargs={'venta_id': 999999}
        )

        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_pdf_tiene_contenido_suficiente(self):
        self.autenticar()
        response = self.client.get(self.url)

        self.assertGreater(len(response.content), 1000)

    def test_total_venta_se_calcula_correctamente(self):
        self.assertEqual(self.venta.total, Decimal('250.00'))