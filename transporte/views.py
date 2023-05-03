from django.shortcuts import render, redirect
from .models import Transporte, Escuela
from .forms import TransporteForm
from django.db.models import Q
from .forms import EscuelaForm
from django.contrib.auth.decorators import login_required
import csv
from django.http import HttpResponse
from openpyxl import Workbook
from openpyxl.writer.excel import save_virtual_workbook
from django.http import FileResponse
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle


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

# aqui van las funciones de exportar a excel, csv y pdf


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
    writer.writerow(['Patente', 'Oferente', 'Cantidad KM',
                    'Alumnos', 'Sectores', 'Escuela', 'URL Mapa'])

    data = Transporte.objects.all().values_list('patente', 'oferente', 'cantidad_km',
                                                'alumnos', 'sectores', 'escuela__nombre', 'url_mapa')
    for row in data:
        writer.writerow(row)

    return response


@login_required
def export_escuelas_excel(request):
    wb = Workbook()
    ws = wb.active
    ws.title = "Escuelas"

    ws.append(['RBD', 'Digito Verificador', 'Nombre'])

    for escuela in Escuela.objects.all():
        ws.append([escuela.rbd, escuela.digito_verificador, escuela.nombre])

    response = HttpResponse(save_virtual_workbook(
        wb), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=escuelas.xlsx'
    return response


@login_required
def export_transportes_excel(request):
    wb = Workbook()
    ws = wb.active
    ws.title = "Transportes"

    ws.append(['Patente', 'Oferente', 'Cantidad KM',
              'Alumnos', 'Sectores', 'Escuela', 'URL Mapa'])

    for transporte in Transporte.objects.all():
        ws.append([transporte.patente, transporte.oferente, transporte.cantidad_km,
                  transporte.alumnos, transporte.sectores, transporte.escuela.nombre, transporte.url_mapa])

    response = HttpResponse(save_virtual_workbook(
        wb), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=transportes.xlsx'
    return response


def export_escuelas_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=escuelas.pdf'

    doc = SimpleDocTemplate(response, pagesize=A4)
    data = [['RBD', 'Digito Verificador', 'Nombre']]

    for escuela in Escuela.objects.all():
        data.append([escuela.rbd, escuela.digito_verificador, escuela.nombre])

    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))

    doc.build([table])
    return response


def export_transportes_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=transportes.pdf'

    doc = SimpleDocTemplate(response, pagesize=A4)
    data = [['Patente', 'Oferente', 'Cantidad KM',
             'Alumnos', 'Sectores', 'Escuela', 'URL Mapa']]

    for transporte in Transporte.objects.all():
        data.append([transporte.patente, transporte.oferente, transporte.cantidad_km,
                    transporte.alumnos, transporte.sectores, transporte.escuela.nombre, transporte.url_mapa])

    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))

    doc.build([table])
    return response
