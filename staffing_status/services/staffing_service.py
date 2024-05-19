import pandas as pd

from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl.styles import Alignment


from django.http import HttpResponse

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
            staffing_status = staffing_status_list.filter(Q(nama=i['pangkat']) | Q(pangkat__nama=i['pangkat'])).first()
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
                message = f"Subsatker {i.subsatker} dengan Pangkat {i.nama} kekurangan {i.dsp - i.rill} personil"
            elif(i.dsp < i.rill) :
                message = f"Subsatker {i.subsatker} dengan Pangkat {i.nama} kelebihan {i.rill - i.dsp} personil"
  
            temp = {
                "dsp" : i.dsp,
                "rill" : i.rill,
                "message" : message
            }
            data[tipe][i.nama] = temp
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
    
    @classmethod
    def get_total_by_pangkat(cls) :
        data = {}

        staffing_status_list = StaffingStatus.objects.all()

        for i in staffing_status_list :
            if(not data.get(i.nama, None)) :
                data[i.nama] = {
                    'dsp' : 0,
                    'rill' : 0,
                }
            
            data[i.nama]['dsp'] = data[i.nama]['dsp'] +  i.dsp
            data[i.nama]['rill'] = data[i.nama]['rill'] + i.rill

        return data

    @classmethod
    def export_csv_file(cls):
        # Define the MultiIndex for columns
        columns = pd.MultiIndex.from_tuples([
            ('', 'No'), ('', 'SatKer'),
            ('POLRI', 'IRJEN DSP'), ('POLRI', 'IRJEN RIIL'),
            ('POLRI', 'BRIGJEN DSP'), ('POLRI', 'BRIGJEN RIIL'),
            ('POLRI', 'KOMBES DSP'), ('POLRI', 'KOMBES RIIL'),
            ('POLRI', 'AKBP DSP'), ('POLRI', 'AKBP RIIL'),
            ('POLRI', 'KOMPOL DSP'), ('POLRI', 'KOMPOL RIIL'),
            ('POLRI', 'AKP DSP'), ('POLRI', 'AKP RIIL'),
            ('POLRI', 'IP DSP'), ('POLRI', 'IP RIIL'),
            ('POLRI', 'BRIG/TA DSP'), ('POLRI', 'BRIG/TA RIIL'),
            ('POLRI', 'Jumlah'),
            ('PNS POLRI', 'IV DSP'), ('PNS POLRI', 'IV RIIL'),
            ('PNS POLRI', 'III DSP'), ('PNS POLRI', 'III RIIL'),
            ('PNS POLRI', 'II/I DSP'), ('PNS POLRI', 'II/I RIIL'),
            ('PNS POLRI', 'Jumlah'), ('', 'Ket')
        ], names=['', ''])

        # Define the data
        data = [
            [1, 'KORLANTAS POLRI', 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 1, 0, 1, '...'],
            [2, 'DIT KAMSEL', 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 1, 0, 1, '...'],
            [3, 'DIT GAKKUM', 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 1, 0, 1, '...'],
            [4, 'DIT REGIDENT', 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 1, 0, 1, '...'],
            [5, 'BAG OPS', 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 1, 0, 1, '...'],
            [6, 'BAG RENMIN', 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 1, 0, 1, '...'],
            [7, 'BAG TIK', 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 1, 0, 1, '...'],
            [8, 'SIKEU', 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 1, 0, 1, '...'],
            [9, 'TAUD', 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 1, 0, 1, '...'],
        ]

        # Create the DataFrame
        df = pd.DataFrame(data, columns=columns)

        # Calculate totals
        totals = [
            ['Jumlah', ''] + [df.iloc[:, i].sum() for i in range(2, len(df.columns)-1)] + ['']
        ]

        # Convert totals to DataFrame
        totals_df = pd.DataFrame(totals, columns=columns)

        # Concatenate the totals row to the original DataFrame
        df = pd.concat([df, totals_df], ignore_index=True)

        # Create an Excel workbook and worksheet
        wb = Workbook()
        ws = wb.active

        # Append the dataframe to the worksheet
        for r in dataframe_to_rows(df, index=False, header=True):
            ws.append(r)

        # Merge cells for the header
        ws.merge_cells('C1:R1')
        ws.merge_cells('S1:X1')

        ws['C1'].value = 'POLRI'
        ws['S1'].value = 'PNS POLRI'

        ws['C1'].alignment = Alignment(horizontal='center', vertical='center')
        ws['S1'].alignment = Alignment(horizontal='center', vertical='center')

        # Align the subheaders
        for col_num, (header, subheader) in enumerate(df.columns, 1):
            cell = ws.cell(row=2, column=col_num)
            cell.alignment = Alignment(horizontal='center', vertical='center')
            cell.value = subheader

        # Adjust column widths
        for col in ws.columns:
            max_length = 0
            column = col[0].column_letter  # Use a normal cell to get the column letter
            for cell in col:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(str(cell.value))
                except:
                    pass
            adjusted_width = max_length + 2
            ws.column_dimensions[column].width = adjusted_width

        # Save the workbook to a virtual file
        from io import BytesIO
        virtual_workbook = BytesIO()
        wb.save(virtual_workbook)

        # Create HTTP response
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="staffing-status.xlsx"'
        response.write(virtual_workbook.getvalue())

        return response