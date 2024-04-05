from abc import ABC, abstractmethod
from personnel_database.models.posisi import Posisi

class PosisiService(ABC):
    
    @classmethod
    def get_all_posisi(cls) :
        posisi_list = Posisi.objects.all()
        return posisi_list