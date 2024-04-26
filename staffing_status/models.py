from django.db import models
from personnel_database.models.subsatker import SubSatKer
from personnel_database.models.pangkat import Pangkat

class StaffingStatus(models.Model) :
    subsatker = models.ForeignKey(SubSatKer, on_delete=models.CASCADE)
    pangkat = models.ForeignKey(Pangkat, on_delete=models.CASCADE)
    dsp = models.IntegerField()
    rill = models.IntegerField()

    def __str__(self) :
        return f"{self.pangkat.nama} ({self.pangkat.tipe}) - {self.subsatker.nama}"