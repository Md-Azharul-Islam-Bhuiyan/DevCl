from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model, authenticate
from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from apps.account.serializers import (
                                      UserRegistrationSerializers, 
                                      UserLoginSerializer,
                                      UpdateCustomerProfileSerializer,
                                      UpdateSellerProfileSerializer,
                                      UpdateUserSerializer
                                      )
from apps.account.models import CustomerProfile, SellerProfile
from apps.account.renderers import UserRenderer
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from rest_framework.authtoken.models import Token
from django.db import transaction

User = get_user_model()


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    access = refresh.access_token
    access['username'] = user.username
    access['email'] = user.email
    access['role'] = user.role
    return {
        'refresh': str(refresh),
        'access': str(access),
    }


class CustomerRegistrationView(APIView):
    serializer_class = UserRegistrationSerializers

    def post(self, request):
        
        serializer = self.serializer_class(data=request.data)
        
        if serializer.is_valid():
            with transaction.atomic():
                validated_data = serializer.validated_data
                user = serializer.save(validated_data)
                user.role = 'CUSTOMER' 
                user.is_active = False
                user.save()
                CustomerProfile.objects.create(customer=user)
                print(user)
                token = default_token_generator.make_token(user)
                print("token ", token)
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                print("uid ", uid)
                confirm_link = f"http://127.0.0.1:8000/api/v1/auth_user/active/{uid}/{token}"
                email_subject = "Confirm Your Email"
                email_body = render_to_string('confirm_email.html', {'confirm_link' : confirm_link})
                
                email = EmailMultiAlternatives(email_subject, '', to=[user.email])
                email.attach_alternative(email_body, "text/html")
                email.send()
            return Response("Check your mail for confirmation", status=status.HTTP_200_OK)
        return Response(serializer.errors)


class SellerRegistrationView(APIView):
    serializer_class = UserRegistrationSerializers

    def post(self, request):
        
        serializer = self.serializer_class(data=request.data)
        
        if serializer.is_valid():
            with transaction.atomic():
                validated_data = serializer.validated_data
                user = serializer.save(validated_data)
                user.role = 'SELLER' 
                user.is_active = False
                user.save()
                SellerProfile.objects.create(seller=user)
                print(user)
                token = default_token_generator.make_token(user)
                print("token ", token)
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                print("uid ", uid)
                confirm_link = f"http://127.0.0.1:8000/api/v1/auth_user/active/{uid}/{token}"
                email_subject = "Confirm Your Email"
                email_body = render_to_string('confirm_email.html', {'confirm_link' : confirm_link})
                
                email = EmailMultiAlternatives(email_subject, '', to=[user.email])
                email.attach_alternative(email_body, "text/html")
                email.send()
            return Response("Check your mail for confirmation", status=status.HTTP_200_OK)
        return Response(serializer.errors)


class ActivateAccountView(APIView):
    def get(self, *args, **kwargs):
        uid64 = kwargs.get('uid64')  
        token = kwargs.get('token')

        try:
            uid = urlsafe_base64_decode(uid64).decode()
            user = User.objects.get(pk=uid)
        except User.DoesNotExist:
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return Response({"message": "Account Successfully Activated"}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Invalid activation link or user does not exist."}, status=status.HTTP_404_NOT_FOUND)


class UserLoginView(APIView):
    renderer_classes = [UserRenderer]

    def post(self, request, format=None):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data.get('email')
        password = serializer.data.get('password')
        user = authenticate(email=email, password=password)
        # print(user.email)
        if user is not None:
            token = get_tokens_for_user(user)
            return Response({'token': token, 'msg': 'Login Success'}, status=status.HTTP_200_OK)
        else:
            return Response({'errors': 'Email or Password is not Valid'}, status=status.HTTP_404_NOT_FOUND)

class UpdateUserView(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UpdateUserSerializer
    

class CustomerRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = CustomerProfile.objects.all()
    serializer_class = UpdateCustomerProfileSerializer


class SellerRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = SellerProfile.objects.all()
    serializer_class = UpdateSellerProfileSerializer