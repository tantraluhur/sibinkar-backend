from django.db import models

from authentication.models.base import BaseModel

from personnel_database.models.users import UserPersonil

class Chart(BaseModel) :
    nama = models.CharField(max_length=120)

class ChartNodes(BaseModel) :
    personil = models.ForeignKey(UserPersonil, on_delete=models.SET_NULL, null=True)
    parent = models.ForeignKey("self")
    offset = models.IntegerField()