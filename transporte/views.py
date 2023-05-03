from django.shortcuts import render, redirect
from .models import Transporte, Escuela
from .forms import TransporteForm
from django.db.models import Q
from .forms import EscuelaForm
from django.contrib.auth.decorators import login_required
import csv
from django.http import HttpResponse
@login_required
def transporte_list(request):
    query = request.GET.get('q', '')
    if query:
        transportes = Transporte.objects.filter(
            Q(patente__icontains=query) |
            Q(oferente__icontains=query) |
            Q(cantidad_km__icontains=query) |
            Q(alumnos__icontains=query) |
            Q(sectores__icontains=query) |
            Q(escuela__nombre__icontains=query)
        )
    else:
        transportes = Transporte.objects.all()
    return render(request, 'transporte/transporte_list.html', {'transportes': transportes})

@login_required
def transporte_create(request):
    if request.method == 'POST':
        form = TransporteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('transporte_list')
    else:
        form = TransporteForm()
    return render(request, 'transporte/transporte_form.html', {'form': form})
@login_required
def transporte_update(request, patente):
    transporte = Transporte.objects.get(patente=patente)
    if request.method == 'POST':
        form = TransporteForm(request.POST, instance=transporte)
        if form.is_valid():
            form.save()
            return redirect('transporte_list')
    else:
        form = TransporteForm(instance=transporte)
    return render(request, 'transporte/transporte_form.html', {'form': form})
@login_required
def transporte_delete(request, patente):
    transporte = Transporte.objects.get(patente=patente)
    transporte.delete()
    return redirect('transporte_list')

@login_required
def escuela_create(request):
    if request.method == 'POST':
        form = EscuelaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('transporte_list')
    else:
        form = EscuelaForm()
    return render(request, 'transporte/escuela_form.html', {'form': form})


@login_required
def profile_view(request):
    return render(request, 'transporte_list.html')
@login_required
def export_escuelas_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="escuelas.csv"'

    writer = csv.writer(response)
    writer.writerow(['RBD', 'Digito Verificador', 'Nombre'])

    data = Escuela.objects.all().values_list('rbd', 'digito_verificador', 'nombre')
    for row in data:
        writer.writerow(row)

    return response
@login_required
def export_transportes_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="transportes.csv"'

    writer = csv.writer(response)
    writer.writerow(['Patente', 'Oferente', 'Cantidad KM', 'Alumnos', 'Sectores', 'Escuela', 'URL Mapa'])

    data = Transporte.objects.all().values_list('patente', 'oferente', 'cantidad_km', 'alumnos', 'sectores', 'escuela__nombre', 'url_mapa')
    for row in data:
        writer.writerow(row)

    return response