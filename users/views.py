from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from .serializers import RegistrationSerializer, LoginSerializer

# Registration API
class RegistrationAPIView(APIView):
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({'id': user.id, 'username': user.username, 'first_name': user.first_name, 'last_name': user.last_name, 'phone': user.phone}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Login API
class LoginAPIView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(username=username, password=password)
            if user:
                return Response({'id': user.id, 'username': user.username, 'first_name': user.first_name, 'last_name': user.last_name, 'phone': user.phone}, status=status.HTTP_200_OK)
            return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .serializers import UserSerializer

from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
## Removed unused imports for deleted serializers
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from django.urls import reverse
from django.conf import settings
from rest_framework import viewsets
from .serializers_profile_role import ProfileSerializer, RoleSerializer
from .models import Profile, Role, UserRole
from rest_framework.decorators import action


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.select_related('user').all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]


class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['post'], url_path='assign', permission_classes=[IsAuthenticated])
    def assign(self, request, pk=None):
        role = self.get_object()
        user_id = request.data.get('user_id')
        if not user_id:
            return Response({'detail': 'user_id required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            from django.contrib.auth import get_user_model
            User = get_user_model()
            user = User.objects.get(pk=user_id)
            UserRole.objects.get_or_create(user=user, role=role)
            return Response({'detail': f'Role {role.name} assigned to user {user.username}'})
        except Exception as exc:
            return Response({'detail': str(exc)}, status=status.HTTP_400_BAD_REQUEST)


class RegisterView(generics.CreateAPIView):
## RegisterView removed


## ChangePasswordView removed

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # Check old password
        if not self.object.check_password(serializer.validated_data.get('old_password')):
            return Response({'old_password': ['Wrong password.']}, status=status.HTTP_400_BAD_REQUEST)
        # Set new password
        self.object.set_password(serializer.validated_data.get('new_password'))
        self.object.save()
        return Response({'detail': 'Password updated successfully.'})



# Commented out LogoutView (blacklist logic removed)
# class LogoutView(APIView):
#     permission_classes = [IsAuthenticated]
#
#     def post(self, request):
#         serializer = LogoutSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         refresh_token = serializer.validated_data['refresh']
#         try:
#             token = RefreshToken(refresh_token)
#             token.blacklist()
#         except Exception:
#             return Response({'detail': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
#         return Response({'detail': 'Logged out successfully'})


## PasswordResetRequestView removed


## PasswordResetConfirmView removed


User = get_user_model()



class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('id')
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    @action(detail=False, methods=['get'], url_path='me', permission_classes=[IsAuthenticated])
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
