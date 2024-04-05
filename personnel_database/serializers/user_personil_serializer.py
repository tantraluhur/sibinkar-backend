from rest_framework import serializers
from personnel_database.models.users import UserPersonil

class UserPersonilSerializer(serializers.ModelSerializer) :
    pangkat = serializers.CharField(source="pangkat.nama")
    subsatker = serializers.CharField(source="subsatker.nama")
    subdit = serializers.CharField(source="subdit.nama")
    posisi = serializers.CharField(source="posisi.nama")
    class Meta:
        model = UserPersonil
        exclude = ['nomor', 'created_at', 'updated_at']