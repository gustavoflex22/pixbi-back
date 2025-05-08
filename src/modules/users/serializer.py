from django.contrib.auth import get_user_model
from rest_framework.serializers import (
    ModelSerializer,
    Serializer,
    CharField,
    BooleanField,
    UUIDField
)


class UserSerializer(ModelSerializer):

    class Meta:
        model = get_user_model()
        fields =("id", "is_superuser", "username", "first_name", "last_name", "email", "is_staff", "is_active", "form_answer", "accepted_terms" )
        # exclude = ["password"]

class PreSaveUserSerializer(ModelSerializer):

    is_automation = BooleanField(default=False, write_only=True)

    class Meta:
        model = get_user_model()
        fields = ["username", "email", "password", "is_automation"]
    
    def create(self, validated_data):
        user = get_user_model().objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
        )
        return user

class FirebaseCustomLogin(Serializer):

    username = CharField()
    password = CharField()

class ChangePasswordSerializer(Serializer):

    current_password = CharField()
    new_password = CharField()

class ForgotPasswordChangePasswordSerializer(Serializer):

    token = UUIDField()
    new_password = CharField()

class ChangeEmailSerializer(Serializer):

    new_email = CharField()

class CheckForgotTokenSerializer(Serializer):

    token = UUIDField()
