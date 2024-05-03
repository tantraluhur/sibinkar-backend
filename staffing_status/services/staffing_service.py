from abc import ABC
from django.db.models import Q
from django.db import transaction

from commons.middlewares.exception import BadRequestException
from staffing_status.models import StaffingStatus
from personnel_database.models.subsatker import SubSatKer

class StaffingService(ABC):
    
    @classmethod
    @transaction.atomic
    def update_staffing_status(cls, **kwargs) :
        subsatker = kwargs.pop("satker")
        data = kwargs.pop("data")
        staffing_status_list = StaffingStatus.objects.filter(subsatker__nama = subsatker)

        if(len(staffing_status_list) == 0) :
            raise BadRequestException(f"Satker {subsatker} not exists in staffing status.")
        
        for i in data :
            i = dict(i)
            staffing_status = staffing_status_list.filter(pangkat__nama=i['pangkat']).first()
            if(not staffing_status) :
                raise BadRequestException(f"Pangkat {i['pangkat']} not exists in staffing status.")
            cls.update_data(staffing_status, i['dsp'])

        return cls.get_staffing_status()

    @classmethod
    def update_data(cls, data: StaffingStatus, dsp: int) :
        data.dsp = dsp
        data.save()


    @classmethod
    def get_staffing_status(cls) :
        data = []
        satker_list = SubSatKer.objects.all()
        for i in satker_list :
            temp_polri = cls.get_staffing_data("POLRI", i)
            temp_pns_polri = cls.get_staffing_data("PNS POLRI", i)
            temp = cls.data_wrapper(i.nama, temp_polri, temp_pns_polri)
            data.append(temp)

        return data

    @classmethod
    def get_staffing_data(cls, tipe: str, subsatker:SubSatKer) :
        data = {
                tipe: {
                    "jumlah" : {
                        "dsp" : 0,
                        "rill" : 0
                    }
                }}
        
        staffing_status_list = StaffingStatus.objects.filter(Q(pangkat__tipe = tipe) & Q(subsatker=subsatker))

        for i in staffing_status_list :
            message = ""
            if(i.dsp > i.rill) :
                message = f"Subsatker {i.subsatker} dengan Pangkat {i.pangkat.nama} kekurangan {i.dsp - i.rill} personil"
            elif(i.dsp < i.rill) :
                message = f"Subsatker {i.subsatker} dengan Pangkat {i.pangkat.nama} kelebihan {i.rill - i.dsp} personil"
  
            temp = {
                "dsp" : i.dsp,
                "rill" : i.rill,
                "message" : message
            }
            data[tipe][i.pangkat.nama] = temp
            data[tipe]['jumlah']['dsp'] = data[tipe]['jumlah']['dsp'] + i.dsp
            data[tipe]['jumlah']['rill'] = data[tipe]['jumlah']['rill'] + i.rill

        return data
    
    @classmethod
    def data_wrapper(cls, satker, polri: dict, pns_polri: dict) :
        data = {"satker" : satker,
                "keterangan" : {
                    "dsp" : polri["POLRI"]["jumlah"]["dsp"] + pns_polri["PNS POLRI"]["jumlah"]["dsp"],
                    "rill" : polri["POLRI"]["jumlah"]["rill"] + pns_polri["PNS POLRI"]["jumlah"]["rill"]
                },
                **polri, **pns_polri
        }
        return data

 
