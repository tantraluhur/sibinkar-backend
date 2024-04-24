from rest_framework import serializers
from personnel_database.models.users import UserPersonil

class UserPersonilSerializer(serializers.ModelSerializer) :
    pangkat = serializers.CharField(source="pangkat.nama")
    subsatker = serializers.CharField(source="subsatker.nama")
    subdit = serializers.CharField(source="subdit.nama")
    jabatan = serializers.CharField(source="jabatan.nama")
    class Meta:
        model = UserPersonil
        exclude = ['nomor', 'created_at', 'updated_at']

class PaginationSerializer(serializers.Serializer) :
    total_pages = serializers.CharField()
    current_page = serializers.CharField()
    limit = serializers.CharField()
    total_item = serializers.CharField()
    has_next = serializers.BooleanField()
    has_previous = serializers.BooleanField()

class UserPersonilPaginationSerializer(serializers.Serializer) :
    result = UserPersonilSerializer(many=True)
    meta = PaginationSerializer()