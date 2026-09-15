from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import LoginSerializer, RegisterSerializer, UserSerializer


class RegisterView(APIView):
    """Create a new user account and return JWT tokens."""

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        tokens = LoginSerializer.get_tokens(user)
        return Response(
            {
                'message': 'Registration successful.',
                'user': UserSerializer(user).data,
                'tokens': tokens,
            },
            status=status.HTTP_201_CREATED,
        )


class LoginView(APIView):
    """
    Authenticate with email + password OR phone_number + password.
    Returns JWT access and refresh tokens.
    """

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        return Response(
            {
                'message': 'Login successful.',
                'user': UserSerializer(user).data,
                'tokens': LoginSerializer.get_tokens(user),
            },
            status=status.HTTP_200_OK,
        )
