from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from commons.applibs.response import prepare_success_response, prepare_error_response, serializer_error_response
from commons.middlewares.exception import APIException

from personnel_database.serializers.user_personil_serializer import UserPersonilSerializer
from personnel_database.services.user_personil_service import UserPersonilService

class PersonilView(APIView) :
    permission_classes = [IsAuthenticated,]
    
    def __init__(self) :
        self.serializer = UserPersonilSerializer
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
        serializer = self.serializer(personil_list, many=True)
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