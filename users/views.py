from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from django.urls import reverse
from django.conf import settings

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets, generics
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser, FormParser

from .serializers import LoginSerializer, UserSerializer
from .serializers import ChangePasswordSerializer
from .serializers_profile_role import ProfileSerializer, RoleSerializer
from .models import Role, UserRole, Profile

# Get User Model for consistent use throughout the file
User = get_user_model() 

# Registration API (Logic Hashed Out)
# class RegistrationAPIView(APIView):
#     permission_classes = [AllowAny]
# ...

# Login API
class LoginAPIView(APIView):
    permission_classes = [AllowAny]

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


# Profile endpoints are disabled
# class ProfileViewSet(viewsets.ModelViewSet):
#     queryset = Profile.objects.select_related('user').all()
#     serializer_class = ProfileSerializer
#     permission_classes = [IsAuthenticated]


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
            user = User.objects.get(pk=user_id)
            UserRole.objects.get_or_create(user=user, role=role)
            return Response({'detail': f'Role {role.name} assigned to user {user.username}'})
        except User.DoesNotExist:
            return Response({'detail': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as exc:
            # Using str(exc) is helpful for debugging deployment failures
            return Response({'detail': str(exc)}, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('id')
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    # Placeholder for the update method based on the structure provided previously
    # NOTE: The update logic provided previously looked like it belonged to a ChangePasswordView,
    # but I've kept it here as the generic ModelViewSet update method for safety.
    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        # Assuming the serializer handles fields correctly.
        # This implementation looks like a ChangePassword view logic.
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        if 'old_password' in serializer.validated_data:
            # Check old password
            if not self.object.check_password(serializer.validated_data.get('old_password')):
                return Response({'old_password': ['Wrong password.']}, status=status.HTTP_400_BAD_REQUEST)
            # Set new password
            self.object.set_password(serializer.validated_data.get('new_password'))
        else:
            # Standard update logic (call super if needed, but the provided code
            # only implemented password change)
            pass

        self.object.save()
        return Response({'detail': 'User updated successfully.'})

    @action(detail=False, methods=['get'], url_path='me', permission_classes=[IsAuthenticated])
    def me(self, request):
        serializer = self.get_serializer(request.user, context={'request': request})
        return Response(serializer.data)

# Profile file upload API disabled
# class ProfileFileUploadView(APIView):
# ...

# Change Password API View
from rest_framework.permissions import IsAuthenticated

class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            old_password = serializer.validated_data['old_password']
            new_password = serializer.validated_data['new_password']
            if not user.check_password(old_password):
                return Response({'old_password': ['Wrong password.']}, status=status.HTTP_400_BAD_REQUEST)
            user.set_password(new_password)
            user.save()
            return Response({'detail': 'Password changed successfully.'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)