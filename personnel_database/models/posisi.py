from django.db import models

from authentication.models.base import BaseModel

class Posisi(BaseModel) :
    nama = models.CharField(max_length=120)
    