from django.db import models

from authentication.models.base import BaseModel

class Jabatan(BaseModel) :
    nama = models.CharField(max_length=240)

    def __str__(self) :
        return self.nama
    