import secrets
import string
from uuid import uuid4

from django.contrib.auth import get_user_model, authenticate
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.db.transaction import atomic
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework import exceptions
from django.conf import settings
from jinja2 import Environment, PackageLoader, select_autoescape
import firebase_admin.auth as auth

from src.modules.users.serializer import (
    UserSerializer,
    PreSaveUserSerializer,
    FirebaseCustomLogin,
    ChangePasswordSerializer,
    CheckForgotTokenSerializer,
    ForgotPasswordChangePasswordSerializer,
    ChangeEmailSerializer
)
from src.modules.shared.service.sendgrid_service import SendgridService


class UserView(ModelViewSet):
    
    queryset = get_user_model().objects.all()
    permission_classes = [AllowAny]
    serializer_class = UserSerializer
    sendgrid_service = SendgridService(
        settings.SENDGRID_API_KEY,
        settings.SENDGRID_FROM_EMAIL,
        ["kennedy@connectingfood.com", "arthur@connectingfood.com"]
    )
    jinja_env = Environment(
        loader=PackageLoader("src"),
        autoescape=select_autoescape()
    )

    @action(["GET"], detail=False, url_name="me", permission_classes=[IsAuthenticated])
    def me(self, request):
        return Response(data=self.serializer_class(instance=request.user).data)
    
    @action(["PATCH"], detail=False, permission_classes=[IsAuthenticated])
    def accept_terms(self, request):
        current_user = request.user
        current_user.accepted_terms = True
        current_user.save()
        return Response(data=self.serializer_class(instance=request.user).data)

    @action(["POST"], detail=False, serializer_class=FirebaseCustomLogin, permission_classes = [AllowAny])
    def firebase_custom_token(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        credentials = {
            "username": serializer.validated_data['username'],
            "password": serializer.validated_data['password'],
        }

        user = authenticate(**credentials)
        
        if user is None:
            raise exceptions.AuthenticationFailed("Usuario ou senha invalidos.")

        if not user.is_active:
            raise exceptions.AuthenticationFailed("Usuario ou senha invalidos.")

        access_token = auth.create_custom_token(user.username)
        return Response(status=status.HTTP_201_CREATED, data={"access": access_token.decode("utf-8")})

    @atomic
    @action(["POST"], detail=False, serializer_class=ChangePasswordSerializer, permission_classes=[IsAuthenticated])
    def change_password(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        current_user = request.user
        
        user = authenticate(username=current_user.username, password=serializer.validated_data["current_password"])
        if not user:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        user.set_password(serializer.validated_data["new_password"])
        user.save()

        auth.update_user(
            current_user.username,
            password=serializer.validated_data["new_password"],
        )

        return Response(status=status.HTTP_204_NO_CONTENT)
    
    @atomic
    @action(["POST"], detail=False, serializer_class=ForgotPasswordChangePasswordSerializer, permission_classes=[AllowAny])
    def forgot_password_change_password(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = get_user_model().objects.filter(forgot_password_uuid=serializer.validated_data["token"])
        if not user:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        user = user.first()

        user.set_password(serializer.validated_data["new_password"])
        user.forgot_password_uuid = None
        user.save()

        auth.update_user(
            user.username,
            password=serializer.validated_data["new_password"],
        )

        return Response(status=status.HTTP_204_NO_CONTENT)
    
    @atomic
    @action(["POST"], detail=False, serializer_class=ChangeEmailSerializer, permission_classes=[IsAuthenticated])
    def change_email(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        current_user = request.user
        
        users_found = get_user_model().objects.filter(email=serializer.validated_data["new_email"])
        if users_found.exists():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        current_user.email = serializer.validated_data["new_email"]
        current_user.save()

        auth.update_user(
            current_user.username,
            email=serializer.validated_data["new_email"],
        )

        return Response(status=status.HTTP_204_NO_CONTENT)
    
    @atomic
    @action(["POST"], detail=False, serializer_class=ChangeEmailSerializer, permission_classes=[AllowAny])
    def send_forgot_password(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user_found = get_user_model().objects.filter(email=serializer.validated_data["new_email"])
        if not user_found.exists():
            return Response(status=status.HTTP_204_NO_CONTENT)
        user_found = user_found.first()
        
        user_found.forgot_password_uuid = uuid4()
        user_found.save()
        
        forgot_password_url = f"{settings.FRONT_BASE_URL}/forms/new_osc/forgot_password/{user_found.forgot_password_uuid}"

        self._send_forgot_password_email(
            forgot_password_url,
            user_found.email,
        )

        return Response(status=status.HTTP_204_NO_CONTENT)
    
    @atomic
    @action(["POST"], detail=False, serializer_class=CheckForgotTokenSerializer, permission_classes=[AllowAny])
    def check_forgot_password_token(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user_found = get_user_model().objects.filter(forgot_password_uuid=serializer.validated_data["token"])
        if not user_found.exists():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @atomic
    @action(["POST"], detail=False, serializer_class=PreSaveUserSerializer)
    def send_pre_save_user(self, request):
        alphabet = string.ascii_letters + string.digits
        password = ''.join(secrets.choice(alphabet) for i in range(20))
        request.data["password"] = password

        serializer = PreSaveUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        firebase_user = auth.create_user(
            uid=serializer.validated_data['username'],
            email=serializer.validated_data['email'],
            password=serializer.validated_data['password']
        )
        access_token = auth.create_custom_token(firebase_user.uid)
        logged_url = f"{settings.FRONT_BASE_URL}/forms/new_osc?auth={access_token.decode('utf-8')}" if serializer.validated_data['is_automation'] else None
        self._send_user_to_email(
            serializer.validated_data.get("username"),
            serializer.validated_data.get("email"),
            password,
            logged_url
        )
        return Response(status=status.HTTP_201_CREATED, data={"access": access_token.decode("utf-8")})
        
    def _send_user_to_email(self, cnpj: str, email: str, password: str, logged_url: str):
        
        template = self.jinja_env.get_template("email/client_user_access_recadastramento.html") if logged_url else self.jinja_env.get_template("email/client_user_access.html")
        
        html_contet = template.render({"cnpj": cnpj, "password": password, "logged_url": logged_url})
        subject = "Atualização Cadastral – Connecting Food" if logged_url else "Seu acesso ConnectingFood chegou!"
        mail, personalization = self.sendgrid_service.get_html_mail(
            email,
            subject,
            html_contet,
            bool(logged_url)
        )
        self.sendgrid_service.send_email(
            mail, personalization
        )
    
    def _send_forgot_password_email(self, change_password_link: str, email: str):
        
        template = self.jinja_env.get_template("email/client_forgot_password.html")
        html_contet = template.render({"change_password_link": change_password_link})
        mail, personalization = self.sendgrid_service.get_html_mail(
            email,
            "Redefinição de senha!",
            html_contet
        )
        self.sendgrid_service.send_email(
            mail, personalization
        )
