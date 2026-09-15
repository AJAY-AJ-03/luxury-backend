from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Public representation of a user (no password fields)."""

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email',
            'phone_number',
            'first_name',
            'last_name',
            'date_joined',
        )
        read_only_fields = fields


class RegisterSerializer(serializers.ModelSerializer):
    """Registration with password confirmation."""

    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
        style={'input_type': 'password'},
    )
    confirm_password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'},
    )

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'phone_number',
            'first_name',
            'last_name',
            'password',
            'confirm_password',
        )

    def validate_email(self, value):
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError('A user with this email already exists.')
        return value.lower()

    def validate_phone_number(self, value):
        if User.objects.filter(phone_number=value).exists():
            raise serializers.ValidationError('A user with this phone number already exists.')
        return value

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError(
                {'confirm_password': 'Passwords do not match.'}
            )
        attrs.pop('confirm_password')
        return attrs

    def create(self, validated_data):
        password = validated_data.pop('password')
        return User.objects.create_user(password=password, **validated_data)


class LoginSerializer(serializers.Serializer):
    """
    Login with a single email_or_phone field plus password.
    """

    email_or_phone = serializers.CharField(required=True)
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'},
    )

    def validate(self, attrs):
        identifier = (attrs.get('email_or_phone') or '').strip()
        password = attrs.get('password')

        if not identifier:
            raise serializers.ValidationError(
                {'email_or_phone': 'Email or phone number is required.'}
            )

        if '@' in identifier:
            user = User.objects.filter(email__iexact=identifier).first()
        else:
            user = User.objects.filter(phone_number=identifier).first()

        if user is None or not user.check_password(password):
            raise serializers.ValidationError('Invalid credentials.')

        if not user.is_active:
            raise serializers.ValidationError('This account has been deactivated.')

        attrs['user'] = user
        return attrs

    @staticmethod
    def get_tokens(user):
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
