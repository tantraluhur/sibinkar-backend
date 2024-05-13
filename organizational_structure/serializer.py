from rest_framework import serializers

from organizational_structure.models import Nodes, Chart

class CreateNodeSerializer(serializers.Serializer) :
    parent_id = serializers.IntegerField()
    nama = serializers.CharField()
    jabatan = serializers.CharField()
    offset = serializers.BooleanField()

class RecursiveSerializer(serializers.Serializer):
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class NodeSerializer(serializers.ModelSerializer) :
    child = RecursiveSerializer(many=True, read_only=True)
    child_offsets = RecursiveSerializer(many=True, read_only=True)
    class Meta:
        model = Nodes
        exclude = ['created_at', 'updated_at']

class ChartSerializer(serializers.ModelSerializer) :
    nodes = NodeSerializer()
    class Meta:
        model = Chart
        exclude = ['created_at', 'updated_at']

class ChartNameSerializer(serializers.ModelSerializer) :

    class Meta:
        model = Chart
        fields = ['id', 'nama']

class CreateChartSerializer(serializers.Serializer) :
    nama_chart = serializers.CharField()
    nama = serializers.CharField()
    jabatan = serializers.CharField()
