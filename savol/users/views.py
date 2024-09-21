from .models import User
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.authentication import JWTAuthentication



class SignupView(APIView):
    serializer_class = SignupSerializer
    permission_classes = (AllowAny,)
    authentication_classes = (JWTAuthentication, )

    def post(self, request, *args, **kwargs):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"id":user.id})
        
        return Response({
                "error": True,
                "message" : serializer.errors })
        



class LoginView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer
    authentication_classes = (JWTAuthentication,)


class LogoutView(APIView):
    serializer_class = LogoutSerializer
    permission_classes = [IsAuthenticated, ]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        try:
            refresh_token = self.request.data['refresh']
            token = RefreshToken(refresh_token)
            token.blacklist()
            data = {
                'success': True,
                'message': "You are loggout out"
            }
            return Response(data, status=205)
        except TokenError:
            return Response(status=400)


class VerifyEmail(APIView):
    permission_classes = (AllowAny, )

    def post(self, request):
        user_id = request.data.get('id', None)
        code = request.data.get('code', None)

        if not code or not user_id:
            return Response({"message": "Tasdiqlash kodini kiritishingiz kerak"}, status=400)
        
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"message": "Invalid user"}, status=400)
        
        is_valid, message = self.check(user, code)
        if not is_valid:
            return Response({"message": message}, status=400)
        tokens = self.get_tokens_for_user(user)
        tokens.update({"message": "Email tasdiqlandi"})
        return Response(tokens)

    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)

        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
    
    @staticmethod
    def check(user, code):
        codes = user.verify.filter(code=code, 
                                   expiration_time__gte=timezone.now(),
                                   is_confirmed=False)

        if not codes.exists():
            return False, "Tasdiqlash kod xato yoki eskirgan"

        user.verified = True
        user.save()

        matched_code = codes.first()
        matched_code.is_confirmed = True
        matched_code.save()

        return True, None


class UserDetailView(APIView):
    permission_classes = (IsAuthenticated, )
    def get(self, request, *args, **kwargs):
        user = request.user
        context = {
            "username": user.username,
        }
        if user.profile.photo:
            context.update({"photo": user.profile.photo.url})
        return Response(context)


class UpdateProfileView(APIView):
    serializer_class = UpdateProfileSerializer
    permission_classes = (IsAuthenticated, )
    def get(self, request, *args, **kwargs):
        pass
    def post(self, request, *args, **kwargs):
        pass

class DashboardView(APIView):
    def get(self, request, *args, **kwargs):
        user = request.user
        context = {
            'first_name':user.first_name,
            'last_name':user.last_name,
            'username':user.username,
            'profile_image':user.profile.photo.url,
            'bio':user.profile.bio,
        }
        return Response(context)


@api_view(['GET'])
@permission_classes([AllowAny])
def UserInfoView(request, username):
    if request.user.username == username:
        user = request.user
        context = {
            'first_name':user.first_name,
            'last_name':user.last_name,
            'username':user.username,
            'bio':user.profile.bio,
            'email':user.email,
            'on_auth':user.is_authenticated,
            'is_current': True,
        }
        if user.profile.photo:
            context.update({"photo":user.profile.photo.url})
    else:
        try:
            user = User.objects.get(username=username)
            context = {
                'first_name':user.first_name,
                'last_name':user.last_name,
                'username':user.username,
                'bio':user.profile.bio,
                'on_auth':user.is_authenticated,
                'is_current': False,
            }
            if (user.profile.photo):
                context.update({
                    'photo':user.profile.photo.url,
                })
        except Exception as e:
            print(e)
            print(username)
            context = {
                'error': "User does not found"
            }
    return Response(context)

class UsersToFollow(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request, *args, **kwargs):
        users = User.objects.exclude(id=request.user.id)[:10]
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

