from django.shortcuts import render, redirect
from .models import Transporte, Escuela
from .forms import TransporteForm
from django.db.models import Q
from .forms import EscuelaForm
from django.contrib.auth.decorators import login_required

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