from io import BytesIO
from django.http import HttpResponse
from django.db.models import Q
from django.db import transaction
from abc import ABC

import pandas as pd

from openpyxl import Workbook
import xlsxwriter


from commons.middlewares.exception import NotFoundException
from commons.applibs.pagination import pagination

from personnel_database.models.users import UserPersonil
from personnel_database.serializers.user_personil_serializer import UserPersonilSerializer
from staffing_status.models import StaffingStatus

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
        
        page = request.GET.get("page", 1)
        limit = request.GET.get("limit", 8)

        if filter_jabatan:
            query |= Q(jabatan_id=filter_jabatan) if filter_jabatan.isdigit() else Q(jabatan__nama=filter_jabatan)

        if filter_pangkat:
            query |= Q(pangkat_id=filter_pangkat) if filter_pangkat.isdigit() else Q(pangkat__nama=filter_pangkat)

        if filter_subsatker:
            query |= Q(subsatker_id=filter_subsatker) if filter_subsatker.isdigit() else Q(subsatker__nama=filter_subsatker)

        if filter_subdit :
            query |= Q(subdit_id=filter_subdit) if filter_subdit.isdigit() else Q(subdit__nama=filter_subdit)

        personil_list = UserPersonil.objects.filter(query).order_by('updated_at')
        data = pagination(personil_list, limit, page)
        return data
    
    @classmethod
    @transaction.atomic
    def update_personil(cls, serializer, personil: UserPersonil) :
        staffing_status = StaffingStatus.objects.filter(Q(pangkat=personil.pangkat) & Q(subsatker=personil.subsatker)).first()
        staffing_status.rill = staffing_status.rill - 1
        staffing_status.save()

        serializer = serializer.save()
        return serializer
    
    @classmethod
    def export_csv_file(cls):
        personil_list = UserPersonil.objects.all().order_by("pangkat")
        col = [f.name for f in UserPersonil._meta.get_fields()[4:]]
        serializer_data = UserPersonilSerializer(personil_list, many=True).data
        df = pd.DataFrame.from_records(serializer_data, columns=col)
        df.insert(0, 'No.', range(1, len(df) + 1))
        
        df.columns = df.columns.str.upper()
        
        # Convert DataFrame to CSV
        csv_content = df.to_csv(index=False, sep=';')

        # Create an Excel file in memory using xlsxwriter
        output = BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        worksheet = workbook.add_worksheet()

        # Define column widths
        column_widths = {
            0: 5,
            1: 30,
            2: 30,
            3: 20,
            4: 60,
            5: 20,
            6: 30,
            7: 30,
            8: 30,
            9: 30
        }

        # Set column widths
        for col_num, width in column_widths.items():
            worksheet.set_column(col_num, col_num, width)

        # Enable text wrapping
        cell_format = workbook.add_format({ 'valign': 'top'})

        # Write CSV data to the worksheet
        reader = pd.read_csv(BytesIO(csv_content.encode('utf-8')), sep=';')
        for row_num, row in enumerate(reader.values):
            for col_num, cell in enumerate(row):
                worksheet.write(row_num + 1, col_num, cell, cell_format)

        # Write the header separately with different formatting if needed
        bold_format = workbook.add_format({'bold': True, 'valign': 'top'})

        for col_num, header in enumerate(reader.columns):
            worksheet.write(0, col_num, header, bold_format)

        # Close the workbook
        workbook.close()
        output.seek(0)

        # Create HTTP response
        response = HttpResponse(output, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="database-personnel.xlsx"'
        
        return response