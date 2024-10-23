from django.shortcuts import render
from django.utils import timezone
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from accounts.models import User, UserConfirmation
from accounts.serializers import RegisterSerializer, RegisterVerifySerializer, ResendVerifyCodeSerializer, LoginSerializer

# Create your views here.
class RegisterAPIView(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            result = serializer.save()
            return Response(result, status=status.HTTP_201_CREATED)
        return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)

class RegisterVerifyAPIView(generics.GenericAPIView):
    serializer_class = RegisterVerifySerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.data['phone_number']
            code = serializer.data['code']
            user = User.objects.filter(phone_number=phone_number).first()
            otp_code = UserConfirmation.objects.filter(code=code).first()
            if otp_code.is_used != False and otp_code.expires < timezone.now():
                return Response({'message': 'code is invalid'})
            otp_code.is_used = True
            user.is_active = True
            user.save()
            otp_code.save()
            return Response({'message': 'code is valid'})
        return Response(serializer.errors)
    
class ResendVerifyCodeAPIView(generics.GenericAPIView):
    serializer_class = ResendVerifyCodeSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid()
        phone_number = serializer.data['phone_number']
        user = User.objects.filter(phone_number=phone_number).first()
        if user is None:
            return Response({'message': 'User not found'})
        code = user.generate_verify_code()
        return Response({'code': code})
    

class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)