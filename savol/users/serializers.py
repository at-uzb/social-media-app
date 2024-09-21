from .models import *
from shared.checking import check_email
from django.core.mail import send_mail
from rest_framework import serializers
from rest_framework.serializers import ValidationError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class SignupSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=150, required=False)
    id = serializers.UUIDField(read_only=True)
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'password', 'password_confirm']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def validate(self, data):
        data = super(SignupSerializer, self).validate(data)
        email = data['email']
        self.validate_email(email)
        self.validate_passwords(data)
        return data

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        if 'username' not in validated_data or not validated_data['username']:
            validated_data['username'] = self.generate_username(validated_data)

        user = super(SignupSerializer, self).create(validated_data)
        user.set_password(validated_data["password"])
        user.save()
        Profile.objects.create(user=user)
        
        verification_code = user.create_verify_code()
        self.send_verification_email(user.email, verification_code)
        
        return user

    def generate_username(self, validated_data):
        first_name = validated_data.get('first_name', 'user')
        last_name = validated_data.get('last_name', 'userovich')
        base_username = f"{first_name}{last_name}".lower()
        unique_username = base_username.lower()
        count = 1
        while User.objects.filter(username=unique_username).exists() or self.is_reserved_or_offensive(unique_username):
            unique_username = f"{base_username}_{count}"
            count += 1
        return unique_username

    def is_reserved_or_offensive(self, username):
        reserved_usernames = ['admin', 'root', 'superuser', 'user']
        return username.lower() in reserved_usernames

    def validate_passwords(self, data):
        password = data.get('password')
        password_confirm = data.get('password_confirm')
        if password != password_confirm:
            raise ValidationError("Passwords do not match.")
        return data
    
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise ValidationError("Email address already exists.")
        return value


    def send_verification_email(self, email, verification_code):
        subject = 'Account Verification'
        message = f'Your verification code is: {verification_code}'
        from_email = 'your_email@example.com' 
        recipient_list = [email]
        send_mail(subject, message, from_email, recipient_list)


class LoginSerializer(TokenObtainPairSerializer):
    username = serializers.CharField(required=False)
    password = serializers.CharField()

    def validate(self, data):
        username = data.get('username')
        if not username:
            raise ValidationError("Ma'lumotlar to'liq kiritlmagan!")
        
        user = None

        if (check_email(username)):
            try:
                user = User.objects.get(email=username)
                if user is None:
                    raise ValidationError("Bu email bilan hech kim ro'yhatdan o'tmagan")
                elif user:
                    username = user.username
                    data['username'] = username
                else: 
                    raise ValidationError("Parolingiz noto'g'ri")
            except Exception as e:
                raise ValidationError(e)
        data = super(LoginSerializer, self).validate(data)
        return data


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()


class UpdateProfileSerializer(serializers.Serializer):
    pass

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id','photo', 'bio']

class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()
    class Meta:
        model = User
        fields = ['username', 'first_name','last_name','profile']