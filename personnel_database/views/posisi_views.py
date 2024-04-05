from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from commons.applibs.response import prepare_success_response, prepare_error_response

from personnel_database.serializers.posisi_serializer import PosisiSerilaizer
from personnel_database.services.posisi_service import PosisiService

class PosisiView(APIView) :
    permission_classes = [IsAuthenticated,]
    
    def __init__(self) :
        self.serializer = PosisiSerilaizer

    def get(self, request) :
        posisi_list = PosisiService.get_all_posisi()
        serializer_data = self.serializer(posisi_list, many=True).data
        return Response(prepare_success_response(serializer_data), status.HTTP_200_OK)