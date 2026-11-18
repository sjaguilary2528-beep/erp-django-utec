# ventas/views.py
"""Vistas de la app ventas — W07 (lectura) y W08 (escritura)."""
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.views.generic import DeleteView, DetailView, ListView

from .forms import DetalleVentaForm, VentaForm
from .models import DetalleVenta, Venta


# --- VISTAS DE LECTURA (W07) ---

class VentaListView(ListView):
    """Lista paginada de ventas en orden cronológico inverso."""

    model               = Venta
    template_name       = 'ventas/index.html'
    context_object_name = 'ventas'
    paginate_by = 20

    def get_queryset(self):
        return Venta.objects.select_related('cliente').order_by('-fecha')


class VentaDetailView(DetailView):
    model = Venta
    template_name = 'ventas/detalle.html'
    context_object_name = 'venta'
    pk_url_kwarg = 'venta_id'

    def get_queryset(self):
        return Venta.objects.select_related('cliente').prefetch_related('detalles__producto')


# --- VISTAS DE ESCRITURA (W08 y W09) ---

@login_required
@permission_required('ventas.add_venta', raise_exception=True)
def crear_venta(request):
    """Crea un encabezado de venta con una línea de detalle."""
    venta_form = VentaForm(request.POST or None)
    detalle_form = DetalleVentaForm(request.POST or None)

    if request.method == 'POST':
        if venta_form.is_valid() and detalle_form.is_valid():
            venta = venta_form.save()
            detalle = detalle_form.save(commit=False)
            detalle.venta = venta
            detalle.save()
            messages.success(
                request,
                f'Venta #{venta.pk} registrada. Total: ${venta.total:.2f}'
            )
            return redirect('ventas:detalle', venta_id=venta.pk)

    return render(request, 'ventas/crear.html', {
        'venta_form': venta_form,
        'detalle_form': detalle_form,
    })


class VentaDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Venta
    template_name = 'ventas/eliminar.html'
    pk_url_kwarg = 'venta_id'
    success_url = reverse_lazy('ventas:lista')
    permission_required = 'ventas.delete_venta'

    def form_valid(self, form):
        pk = self.object.pk
        response = super().form_valid(form)
        messages.success(self.request, f'Venta #{pk} eliminada.')
        return response

@login_required
def venta_pdf(request, venta_id: int) -> HttpResponse:
    """Genera y descarga la factura de una venta en formato PDF.

    Motor: WeasyPrint (requiere Docker o Linux con libpango/cairo/gdk-pixbuf).
    Alternativa de entorno sin Docker: ver Guía W12 original con xhtml2pdf.

    Args:
        request:  HttpRequest de Django.
        venta_id: ID de la venta a generar.

    Returns:
        HttpResponse con Content-Type application/pdf y descarga directa.

    Raises:
        Http404: si la venta no existe.
    """
    import weasyprint   # import local: solo disponible en Docker/Linux

    from datetime import date
    from django.template.loader import render_to_string
    from configuracion.models  import ConfiguracionERP

    venta = get_object_or_404(
        Venta.objects
        .select_related('cliente')
        .prefetch_related('detalles__producto__categoria'),
        pk=venta_id
    )

    config  = ConfiguracionERP.get_instance()
    context = {
        'venta':  venta,
        'config': config,
        'hoy':    date.today(),
    }

    html_string = render_to_string(
        'ventas/factura_pdf.html',
        context,
        request=request   # necesario para template tags que usen request
    )

    # ── WeasyPrint: conversión HTML → PDF ─────────────────────────────
    # base_url: permite que WeasyPrint encuentre imágenes relativas
    # como /media/productos/logo.jpg o /static/css/factura.css.
    # Sin base_url, las imágenes aparecen en blanco en el PDF.
    pdf_bytes = weasyprint.HTML(
        string   = html_string,
        base_url = request.build_absolute_uri('/'),
    ).write_pdf()

    response = HttpResponse(pdf_bytes, content_type='application/pdf')
    response['Content-Disposition'] = (
        f'attachment; filename="factura_{venta.pk:05d}.pdf"'
    )
    return response
