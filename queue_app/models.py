from django.db import models

class Antrian(models.Model):
    STATUS_PILIHAN = [
        ('Menunggu', 'Menunggu'),
        ('Dikerjakan', 'Dikerjakan'),
        ('Selesai', 'Selesai'),
    ]
    
    nama_pelanggan = models.CharField(max_length=100)
    tipe_hp = models.CharField(max_length=100)
    keluhan = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_PILIHAN, default='Menunggu')
    tanggal_masuk = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nama_pelanggan} - {self.tipe_hp}"
