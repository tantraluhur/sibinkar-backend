import enum
import uuid

from django.db import models

from authentication.models.base import BaseModel
from personnel_database.models.pangkat import Pangkat
from personnel_database.models.subsatker import SubSatKer
from personnel_database.models.subdit import SubDit
from personnel_database.models.jabatan import Jabatan

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
        
    class BKO(str, enum.Enum) :
        GASUS_MASUK = "Gasus masuk"
        GASUM_MASUK = "Gasum masuk"

        @classmethod
        def choices(cls):
            return [(item.value, item.name) for item in cls]
        
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True)
    nama = models.CharField(max_length=120)
    jenis_kelamin = models.CharField(max_length=12, choices=JenisKelamin.choices())
    nrp = models.BigIntegerField()
    pangkat = models.ForeignKey(Pangkat, on_delete=models.CASCADE)
    jabatan = models.ForeignKey(Jabatan, on_delete=models.CASCADE)
    subsatker = models.ForeignKey(SubSatKer, on_delete=models.CASCADE)
    subdit = models.ForeignKey(SubDit, on_delete=models.CASCADE)
    bko = models.CharField(max_length=12, choices=BKO.choices())
    status = models.CharField(max_length=20, choices=Status.choices())

    def __str__(self) :
        return self.nama