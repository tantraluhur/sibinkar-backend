from authentication.models import AuthUser
from rest_framework.authentication import BaseAuthentication


class UserAuthentication(BaseAuthentication):

    """
    This allows authentication
    with either a phone_number or email.
    """

    def authenticate(self, phone_number=None, password=None, **kwargs):

        if phone_number is None:
            email = kwargs.get('email')
            if email is None:
                return None
            else:
                try:
                    user = AuthUser.objects.get(email=email)
                except AuthUser.DoesNotExist:
                    return None
        else:
            try:
                user = AuthUser.objects.get(phone_number=phone_number)

            except AuthUser.DoesNotExist:
                return None

        if user.check_password(password):
            return user

    def get_user(self, user_id):
        try:
            return AuthUser.objects.get(id=user_id)
        except AuthUser.DoesNotExist:
            return None


user_model = UserAuthentication()
