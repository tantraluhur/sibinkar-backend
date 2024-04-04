import enum

from django.db import models

from authentication.models.base import BaseModel
from personnel_database.models.pangkat import Pangkat
from personnel_database.models.posisi import Posisi
from subsatker.models import SubSatKer
from subdit.models import SubDit

class UserPersonil(BaseModel) :

    class JenisKelamin(int, enum.Enum):
        L = 1
        P = 2

        @classmethod
        def choices(cls):
            return [(item.value, item.name) for item in cls]
    
    class Status(int, enum.Enum) :
        AKTIF = 1
        NON_AKTIF = 2
        CUTI = 3
        PENSIUN = 4

        @classmethod
        def choices(cls):
            return [(item.value, item.name) for item in cls]

    nomor = models.IntegerChoices(null=True, blank=True)
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