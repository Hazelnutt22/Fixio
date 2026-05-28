from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Antrian

# ============================
# AUTENTIKASI ADMIN
# ============================

def admin_login(request):
    error_message = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard_statistik')
        else:
            error_message = 'Username atau password salah!'
    return render(request, 'queue_app/login.html', {'error_message': error_message})

def admin_logout(request):
    logout(request)
    return redirect('daftar_antrian')

# ============================
# HALAMAN PUBLIK (USER)
# ============================

# 1. Halaman Utama (Pendaftaran & Antrian Aktif)
def daftar_antrian(request):
    if request.method == 'POST':
        nama = request.POST.get('nama')
        tipe = request.POST.get('tipe')
        keluhan = request.POST.get('keluhan')
        
        Antrian.objects.create(nama_pelanggan=nama, tipe_hp=tipe, keluhan=keluhan)
        return redirect('daftar_antrian')

    # Hanya menampilkan yang belum 'Selesai' di halaman depan
    antrian_aktif = Antrian.objects.exclude(status='Selesai').order_by('-tanggal_masuk')
    return render(request, 'queue_app/index.html', {'semua_antrian': antrian_aktif})

# ============================
# HALAMAN ADMIN (LOGIN REQUIRED)
# ============================

# 2. Halaman Dashboard Statistik & Kontrol Admin Ringan
@login_required
def dashboard_statistik(request):
    semua = Antrian.objects.all()
    
    # Hitung data untuk counter box
    total_antrian = semua.count()
    menunggu = semua.filter(status='Menunggu').count()
    dikerjakan = semua.filter(status='Dikerjakan').count()
    selesai = semua.filter(status='Selesai').count()
    
    # Mengambil 5 antrian terbaru untuk tabel ringkasan
    antrian_terbaru = semua.order_by('-tanggal_masuk')[:5]

    konteks = {
        'total': total_antrian,
        'menunggu': menunggu,
        'dikerjakan': dikerjakan,
        'selesai': selesai,
        'antrian_terbaru': antrian_terbaru
    }
    return render(request, 'queue_app/dashboard.html', konteks)

# 3. Halaman Riwayat Semua Antrian (Termasuk yang Selesai)
@login_required
def riwayat_antrian(request):
    riwayat = Antrian.objects.all().order_by('-tanggal_masuk')
    return render(request, 'queue_app/riwayat.html', {'riwayat': riwayat})

# 4. Fitur Mengubah Status Langsung dari Halaman Aplikasi
@login_required
def ubah_status(request, pk, status_baru):
    antrian = get_object_or_404(Antrian, pk=pk) # <-- Ubah ini juga jadi 404
    antrian.status = status_baru
    antrian.save()
    return redirect(request.META.get('HTTP_REFERER', 'daftar_antrian'))

# Fungsi untuk menghapus data antrian
@login_required
def hapus_antrian(request, pk):
    antrian = get_object_or_404(Antrian, pk=pk)
    antrian.delete() # Menghapus data dari database
    return redirect(request.META.get('HTTP_REFERER', 'daftar_antrian'))

# 5. Fitur Mengubah (Edit) Data Antrian
@login_required
def edit_antrian(request, pk):
    antrian = get_object_or_404(Antrian, pk=pk)
    if request.method == 'POST':
        antrian.nama_pelanggan = request.POST.get('nama')
        antrian.tipe_hp = request.POST.get('tipe')
        antrian.keluhan = request.POST.get('keluhan')
        antrian.save()
        return redirect('riwayat_antrian')
    
    return render(request, 'queue_app/edit_antrian.html', {'antrian': antrian})