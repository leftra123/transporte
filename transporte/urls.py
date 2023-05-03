from django.urls import path
from . import views

urlpatterns = [
    path('', views.transporte_list, name='transporte_list'),
    path('create/', views.transporte_create, name='transporte_create'),
    path('update/<str:patente>/', views.transporte_update, name='transporte_update'),
    path('delete/<str:patente>/', views.transporte_delete, name='transporte_delete'),
    path('escuela/create/', views.escuela_create, name='escuela_create'),
    path('export/escuelas/csv/', views.export_escuelas_csv, name='export_escuelas_csv'),
    path('export/transportes/csv/', views.export_transportes_csv, name='export_transportes_csv'),
]
