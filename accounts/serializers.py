from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from accounts.models import User, UserConfirmation, Intro

class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField()
    phone_number = serializers.CharField()
    password = serializers.CharField()
    confirm_password = serializers.CharField()

    def validate(self, data):
        password=data.get('password')
        confirm_password=data.get('confirm_password')

        if password != confirm_password:
            raise serializers.ValidationError("Confirmation password didn't match")
        return data
    
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            phone_number=validated_data['phone_number'],
            password=make_password(validated_data['password']),
            is_active = False,
        )
        code = user.generate_verify_code()
        return {
            'message': 'Verification code is sent to your phone number',
            'code': code
        }
    
class RegisterVerifySerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    code = serializers.CharField(min_length=5, max_length=5)

class ResendVerifyCodeSerializer(serializers.Serializer):
    phone_number = serializers.CharField()

class LoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        phone_number = data.get('phone_number')
        password = data.get('password')
        user = authenticate(phone_number=phone_number, password=password)
        if not user:
            raise serializers.ValidationError('Invalid phone number or password')
        if not user.is_active:
            raise serializers.ValidationError('User not found')
        return {
            'user': user,
        }
