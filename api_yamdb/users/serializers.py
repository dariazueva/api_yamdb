from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainSerializer

from users.models import CustomUser

from rest_framework.validators import UniqueValidator
from django.core.validators import RegexValidator

USERNAME_REGEX = r"^[\w.@+-]+$"

class CustomUserSerializer(serializers.ModelSerializer):
    """Сериализатор кастомного пользователя."""

    email = serializers.EmailField(
        max_length=254,
        required=True,
        validators=[UniqueValidator(queryset=CustomUser.objects.all())],
    )

    username = serializers.CharField(
        max_length=150,
        required=True,
        validators=[
            UniqueValidator(queryset=CustomUser.objects.all()),
            RegexValidator(
                regex=USERNAME_REGEX,
                message="Имя пользователя может содержать "
                "только буквы, цифры и следующие символы: "
                "@/./+/-/_",
            ),
        ],
    )

    class Meta:
        model = CustomUser
        fields = (
            "username", "email", "first_name", "last_name", "bio", "role"
        )

    def validate(self, attrs):
        data = super().validate(attrs)
        if "username" in data:
            if data["username"].lower() == "me":
                raise serializers.ValidationError("<me> can't be a username")

        return data


class UserRegistrationSerializer(CustomUserSerializer):
    """Сериализатор для модели пользователя."""

    class Meta:
        model = CustomUser
        fields = ("username", "email")
    
    def create(self, validated_data):
        user = CustomUser(
            email=validated_data['email'],
            username=validated_data['username']
        )
        user.save()
        return user


class CustomTokenObtainSerializer(TokenObtainSerializer):
    """Получение токена."""

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        return token

