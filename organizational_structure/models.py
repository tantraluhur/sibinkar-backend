from django.db import models
from django.contrib.postgres.fields import ArrayField

from authentication.models.base import BaseModel

from personnel_database.models.users import UserPersonil

class Nodes(BaseModel) :
    nama = models.CharField(max_length=120)
    jabatan = models.CharField(max_length=120)
    offset = models.BooleanField(default=False)
    child = models.ManyToManyField("self", symmetrical=False, related_name="child_list", blank=True)
    child_offsets = models.ManyToManyField("self", symmetrical=False, related_name="child_offsets_list", blank=True)

class Chart(BaseModel) :
    nama = models.CharField(max_length=120)
    nodes = models.ForeignKey(Nodes, on_delete=models.CASCADE)
