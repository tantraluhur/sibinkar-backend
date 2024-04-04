from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from commons.applibs.response import prepare_success_response, prepare_error_response

class PosisiView(APIView) :
    permission_classes = [IsAuthenticated,]

    def get(self, request) :
        pass