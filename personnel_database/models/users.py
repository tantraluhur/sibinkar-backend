import enum

from django.db import models

from authentication.models.base import BaseModel
from personnel_database.models.pangkat import Pangkat
from personnel_database.models.posisi import Posisi
from personnel_database.models.subsatker import SubSatKer
from personnel_database.models.subdit import SubDit

class UserPersonil(BaseModel) :

    class JenisKelamin(str, enum.Enum):
        L = "L"
        P = "P"

        @classmethod
        def choices(cls):
            return [(item.value, item.name) for item in cls]
    
    class Status(str, enum.Enum) :
        AKTIF = "Aktif"
        NON_AKTIF = "Non Aktif"
        CUTI = "Cuti"
        PENSIUN = "Pensiun"

        @classmethod
        def choices(cls):
            return [(item.value, item.name) for item in cls]

    nomor = models.BigIntegerField(null=True, blank=True)
    nama = models.CharField(max_length=120)
    jenis_kelamin = models.CharField(max_length=12, choices=JenisKelamin.choices())
    nrp = models.BigIntegerField()
    pangkat = models.ForeignKey(Pangkat, on_delete=models.CASCADE)
    jabatan = models.CharField(max_length=220)
    subsatker = models.ForeignKey(SubSatKer, on_delete=models.CASCADE)
    subdit = models.ForeignKey(SubDit, on_delete=models.CASCADE)
    posisi = models.ForeignKey(Posisi, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=Status.choices())
    '''
    subsatker + subdit, pemimpinin
    find by subsatker + subdit, find by posisi anggota
    pemimpin,
    children : [
        anggota,
        anggota
    ]
    '''

    def __str__(self) :
        return self.nama