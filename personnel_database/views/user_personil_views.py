import csv
from django.http import HttpResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

import pandas as pd

from personnel_database.models.users import UserPersonil

from commons.applibs.response import prepare_success_response, prepare_error_response, serializer_error_response
from commons.middlewares.exception import APIException

from personnel_database.serializers.user_personil_serializer import UserPersonilSerializer, UserPersonilPaginationSerializer
from personnel_database.services.user_personil_service import UserPersonilService

class PersonilView(APIView) :
    permission_classes = [IsAuthenticated,]
    
    def __init__(self) :
        self.serializer = UserPersonilSerializer
        self.user_serializer_pagination = UserPersonilPaginationSerializer
        self.service = UserPersonilService

    def post(self, request) :
        try :
            serializer = self.serializer(data=request.data)
            if(not serializer.is_valid()) :
                return Response(serializer_error_response(serializer.errors), status.HTTP_400_BAD_REQUEST)
            user = self.service.add_personil(**serializer.data)
            serializer_data = self.serializer(user).data
            return Response(prepare_success_response(serializer_data), status.HTTP_201_CREATED)
        except APIException as e :
            return Response(prepare_error_response(str(e)), e.status_code)
        except Exception as e :
            return Response(prepare_error_response(str(e)), status.HTTP_500_INTERNAL_SERVER_ERROR)

    
    def get(self, request) :
        personil_list = self.service.get_personil(request)
        serializer = self.user_serializer_pagination(personil_list)
        return Response(prepare_success_response(serializer.data), status.HTTP_200_OK)
    
    def put(self, request, personil_id) :
        try :
            personil = self.service.get_personil_by_id(personil_id)
            serializer = self.serializer(personil, data=request.data, partial=True)
            if(not serializer.is_valid()) :
                return Response(serializer_error_response(serializer.errors), status.HTTP_400_BAD_REQUEST)
            serializer.save()
            return Response(prepare_success_response(serializer.data), status.HTTP_200_OK)
        except APIException as e :
            return Response(prepare_error_response(str(e)), e.status_code)
        except Exception as e :
            return Response(prepare_error_response(str(e)), status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def delete(self, request, personil_id) :
        try :
            personil = self.service.delete_personil(personil_id)
            serializer = self.serializer(personil)
            return Response(prepare_success_response(serializer.data), status.HTTP_200_OK)
        except APIException as e :
            return Response(prepare_error_response(str(e)), e.status_code)
        except Exception as e :
            return Response(prepare_error_response(str(e)), status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class PersonilExport(APIView) :
    permission_classes = [IsAuthenticated,]

    def __init__(self) :
        self.serializer = UserPersonilSerializer
        self.service = UserPersonilService

    def get(self, request) :
        response = self.service.export_csv_file()
        return response