from abc import ABC, abstractmethod
from django.db.models import Q

from commons.middlewares.exception import NotFoundException

from personnel_database.models.users import UserPersonil

class UserPersonilService(ABC):
    
    @classmethod
    def add_personil(cls, **data) :
        pangkat = data.pop('pangkat')
        subsatker = data.pop('subsatker')
        subdit = data.pop('subdit')
        jabatan = data.pop('jabatan')

        personil = UserPersonil.objects.create(**data, pangkat_id = pangkat, subsatker_id = subsatker, 
                                               subdit_id=subdit, jabatan_id = jabatan)
        return personil
    
    @classmethod
    def get_personil_by_id(cls, personil_id) :
        personil = UserPersonil.objects.filter(id=personil_id).first()
        
        if(not personil) :
            raise NotFoundException(f"Personil with id {personil_id} not exists.")

        return personil
    
    @classmethod
    def delete_personil(cls, personil_id) :
        personil = cls.get_personil_by_id(personil_id)

        personil.delete()
        return personil
    

    @classmethod
    def get_personil(cls, request) :
        query = Q()
        filter_jabatan = request.GET.get("jabatan", None)
        filter_pangkat = request.GET.get("pangkat", None)
        filter_subsatker = request.GET.get("subsatker", None)
        filter_subdit= request.GET.get("subdit", None)

        if filter_jabatan:
            query |= Q(jabatan_id=filter_jabatan) if filter_jabatan.isdigit() else Q(jabatan__nama=filter_jabatan)

        if filter_pangkat:
            query |= Q(pangkat_id=filter_pangkat) if filter_pangkat.isdigit() else Q(pangkat__nama=filter_pangkat)

        if filter_subsatker:
            query |= Q(subsatker_id=filter_subsatker) if filter_subsatker.isdigit() else Q(subsatker__nama=filter_subsatker)

        if filter_subdit :
            query |= Q(subdit_id=filter_subdit) if filter_subdit.isdigit() else Q(subdit__nama=filter_subdit)

        personil_list = UserPersonil.objects.filter(query)
        return personil_list