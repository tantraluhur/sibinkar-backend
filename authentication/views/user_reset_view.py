import logging

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from applibs.response import prepare_success_response, prepare_error_response
from authentication.models import AuthUser
from authentication.serializers.password_serializer import ResetPasswordSerializer

logger = logging.getLogger('general')


class ResetPassword(APIView):

    def __init__(self):
        super(ResetPassword, self).__init__()
        self.serializer = ResetPasswordSerializer

    def post(self, request):
        serializer = self.serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            user = AuthUser.objects.get_user_by_phone(serializer.validated_data['phone_number'])
            password = serializer.validated_data['password']

            if not user:
                return Response(prepare_error_response(NOT_VALID_USER))

            if not otp_verify.data.get('success'):
                logger.error(f'otp for reset password {otp_verify.data}')
                return Response(prepare_error_response(otp_verify.data), status.HTTP_200_OK)

            AuthUser.objects.reset_password(phone_number=user.phone_number, password=password)
            return Response(prepare_success_response(), status.HTTP_200_OK)

        except Exception as ex:
            logger.error(ex)
            return Response(prepare_error_response(serializer.errors), status=status.HTTP_400_BAD_REQUEST)
