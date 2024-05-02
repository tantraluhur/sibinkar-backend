from django.db import models

from authentication.models.base import BaseModel

from personnel_database.models.jabatan import Jabatan

class Chart(BaseModel) :
    nama = models.CharField(max_length=120)

class ChartNodes(BaseModel) :
    nama = models.CharField(max_length=120)
    jabatan = models.ForeignKey(Jabatan, on_delete=models.Case)
    parent = models.ForeignKey("self")
    offset = models.IntegerField()