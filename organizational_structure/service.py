from abc import ABC
from django.db import transaction

from commons.middlewares.exception import BadRequestException

from organizational_structure.models import Chart, Nodes

class OrganizationalStructureService(ABC):
    
    @classmethod
    @transaction.atomic
    def create_chart(cls, **data) :
        nama = data.pop('nama_chart')
        nodes = Nodes.objects.create(**data)
        chart = Chart.objects.create(nama=nama, nodes=nodes)

        return chart

    @classmethod
    @transaction.atomic
    def get_chart(cls, chart_id) :
        chart = Chart.objects.filter(id = chart_id).first()

        if(not chart) :
            raise BadRequestException(f"Chart with id {chart_id} not exists.")
        
        return chart
    
    @classmethod
    def get_all_chart_name(cls) :
        chart = Chart.objects.all()
        return chart
    
    @classmethod
    def update_nodes(cls, nodes_id, **data) :
        nodes = Nodes.objects.filter(id=nodes_id).first()

        if(not nodes) :
            raise BadRequestException(f"Nodes with id {nodes_id} not exists.")
        
        for key, value in data.items():
            setattr(nodes, key, value)
        nodes.save()
        return nodes

    @classmethod
    @transaction.atomic
    def create_child_node(cls, chart_id, **data) :
        parent_id = data.pop('parent_id')
        parent_node = Nodes.objects.filter(id=parent_id).first()

        if(not parent_node) :
            raise BadRequestException(f"Node with id {parent_id} not exists.")
        
        chart = cls.get_chart(chart_id)
        child_node = Nodes.objects.create(**data)
        parent_node.child.add(child_node)

        return chart
    
    @classmethod
    @transaction.atomic
    def create_child_offsets_node(cls, chart_id, **data) :
        parent_id = data.pop('parent_id')
        parent_node = Nodes.objects.filter(id=parent_id).first()

        if(not parent_node) :
            raise BadRequestException(f"Node with id {parent_id} not exists.")
        
        chart = cls.get_chart(chart_id)
        child_node = Nodes.objects.create(**data)
        parent_node.child_offsets.add(child_node)

        return chart 
