from django.urls import path
from . import views

urlpatterns = [
    path('', views.daftar_antrian, name='daftar_antrian'),
    path('dashboard/', views.dashboard_statistik, name='dashboard_statistik'),
    path('riwayat/', views.riwayat_antrian, name='riwayat_antrian'),
    path('status/<int:pk>/<str:status_baru>/', views.ubah_status, name='ubah_status'),
    path('edit/<int:pk>/', views.edit_antrian, name='edit_antrian'),
    path('hapus/<int:pk>/', views.hapus_antrian, name='hapus_antrian'),
]