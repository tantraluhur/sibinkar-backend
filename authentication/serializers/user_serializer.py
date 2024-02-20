from django.contrib.auth.models import update_last_login
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from authentication.models.custom_users import user_model
from authentication.models.users import AuthUser


class RegisterSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(max_length=15,
                                         validators=[UniqueValidator(
                                             queryset=AuthUser.objects.filter(is_active=True))])
    password = serializers.CharField(min_length=6)
    name = serializers.CharField(required=False, max_length=50)

    class Meta:
        model = AuthUser
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True},
        }


class LoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField(required=False, max_length=15)
    email = serializers.CharField(required=False, max_length=100)
    password = serializers.CharField()

    def validate(self, attrs):
        phone_number = attrs.get("phone_number", None)
        email = attrs.get("email", None)
        password = attrs.get("password", None)

        user_data = {}
        if not phone_number and not email:
            raise serializers.ValidationError(
                {"phone_number or email": "email or phone_number can not be empty."})

        if phone_number:
            user_data = dict(phone_number=phone_number, password=password)

        if email:
            user_data = dict(email=email, password=password)

        user = user_model.authenticate(**user_data)

        if not user:
            raise serializers.ValidationError(
                {"user": 'phone_number and password is not match.'})
        token = RefreshToken.for_user(user)
        update_last_login(None, user)
        response_data = {
            'token': str(token.access_token),
            'refresh_token': str(token),

        }

        return response_data
