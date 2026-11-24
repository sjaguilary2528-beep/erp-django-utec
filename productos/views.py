# productos/views.py
"""Vistas de la app productos — W07 y W08."""
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Producto
from .forms import ProductoForm
from django.http import HttpResponse
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill
from django.contrib.auth.decorators import login_required


# --- VISTAS DE LECTURA (W07) ---

class ProductoListView(ListView):
    model = Producto
    template_name = 'productos/lista.html'
    context_object_name = 'productos'
    paginate_by = 20

    def get_queryset(self):
        return (
            Producto.objects
            .select_related('categoria', 'proveedor')
            .filter(activo=True)
            .order_by('nombre')
        )


class ProductoDetailView(DetailView):
    model = Producto
    template_name = 'productos/detalle.html'
    context_object_name = 'producto'
    pk_url_kwarg = 'producto_id'

    def get_queryset(self):
        return Producto.objects.select_related('categoria', 'proveedor')


# --- VISTAS DE ESCRITURA (W08) ---

class ProductoCreateView(LoginRequiredMixin, CreateView):
    model = Producto
    form_class = ProductoForm
    template_name = 'productos/crear.html'
    success_url = reverse_lazy('productos:lista')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(
            self.request,
            f'Producto "{self.object.nombre}" creado exitosamente.'
        )
        return response


class ProductoUpdateView(LoginRequiredMixin, UpdateView):
    model = Producto
    form_class = ProductoForm
    template_name = 'productos/editar.html'
    pk_url_kwarg = 'producto_id'
    success_url = reverse_lazy('productos:lista')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(
            self.request,
            f'Producto "{self.object.nombre}" actualizado.'
        )
        return response


class ProductoDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Producto
    template_name = 'productos/eliminar.html'
    pk_url_kwarg = 'producto_id'
    success_url = reverse_lazy('productos:lista')
    permission_required = 'productos.delete_producto'

    def form_valid(self, form):
        nombre = self.object.nombre
        response = super().form_valid(form)
        messages.success(self.request, f'Producto "{nombre}" eliminado.')
        return response


# --- EXPORTACIÓN EXCEL (W12) ---

@login_required
def exportar_excel(request):
    wb = Workbook()
    ws = wb.active
    ws.title = "Productos"

    encabezados = [
        "Nombre", "Precio", "Stock", "Categoría",
        "Proveedor", "Activo", "Fecha de registro"
    ]
    ws.append(encabezados)

    for celda in ws[1]:
        celda.font = Font(bold=True, color="FFFFFF")
        celda.fill = PatternFill(
            start_color="0A2342",
            end_color="0A2342",
            fill_type="solid"
        )

    productos = Producto.objects.select_related(
        "categoria", "proveedor"
    ).all().order_by("nombre")

    for producto in productos:
        ws.append([
            producto.nombre,
            float(producto.precio),
            producto.stock,
            producto.categoria.nombre,
            producto.proveedor.nombre if producto.proveedor else "",
            "Sí" if producto.activo else "No",
            producto.creado.strftime("%d/%m/%Y %H:%M"),
        ])

    response = HttpResponse(
        content_type=(
            "application/vnd.openxmlformats-officedocument."
            "spreadsheetml.sheet"
        )
    )
    response["Content-Disposition"] = (
        'attachment; filename="productos.xlsx"'
    )

    wb.save(response)
    return response
