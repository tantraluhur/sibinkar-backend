from rest_framework import serializers
from personnel_database.models.posisi import Posisi

class PosisiSerilaizer(serializers.ModelSerializer) :
    class Meta:
        model = Posisi
        fields = ['id', 'nama']