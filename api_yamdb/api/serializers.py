from django.core.validators import RegexValidator
from rest_framework import serializers
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainSerializer

from api.utils import Util
from users.models import CustomUser

from django.contrib.auth.tokens import default_token_generator
# from random import randint
import re


USERNAME_REGEX = r'^[\w.@+-]+$'


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
                message='Имя пользователя может содержать '
                'только буквы, цифры и следующие символы: '
                '@/./+/-/_',
            ),
        ],
    )

    class Meta:
        model = CustomUser
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )

    def validate(self, attrs):
        data = super().validate(attrs)
        if 'username' in data:
            if data['username'].lower() == 'me':
                raise ValidationError('<me> can not be a username')
        return data


class UserRegistrationSerializer(serializers.Serializer):
    """Сериализатор для модели пользователя."""
    email = serializers.EmailField(
        max_length=254,
        required=True,
    )

    username = serializers.CharField(
        max_length=150,
        required=True,
        validators=[
            RegexValidator(
                regex=USERNAME_REGEX,
                message='Имя пользователя может содержать '
                'только буквы, цифры и следующие символы: '
                '@/./+/-/_',
            ),
        ],
    )

    class Meta:
        fields = ('username', 'email')

    def create(self, validated_data):
        username = validated_data['username']
        email = validated_data['email']

        user, created = CustomUser.objects.get_or_create(
            username=username,
            email=email
        )
        confirmation_code = default_token_generator.make_token(user)
        Util.send_mail(validated_data['email'], confirmation_code)
        return user

    def validate(self, data):
        username = data.get('username')
        if username:
            if username == 'me' or not re.match(USERNAME_REGEX, username):
                raise ValidationError('<me> can not be a username')
        return data


class CustomTokenObtainSerializer(TokenObtainSerializer):
    """Получение токена."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields[self.username_field] = serializers.CharField()
        self.fields['confirmation_code'] = serializers.CharField()
        self.fields.pop('password', None)

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        return token

    def validate(self, attrs):
        user = CustomUser.objects.filter(
            username=attrs[self.username_field],
        ).first()
        if not user:
            raise NotFound(
                {'username': 'Пользователь с таким username не существует'},
                code='user_not_found',
            )
        if str(user.confirmation_code) != attrs['confirmation_code']:
            raise ValidationError(
                {'confirmation_code': 'Неверный код подтверждения'},
                code="invalid_confirmation_code",
            )
        self.user = user
        user.save()
        return {'token': str(self.get_token(self.user).access_token)}


class CustomUserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        validators=[
            UniqueValidator(queryset=CustomUser.objects.all()),
            RegexValidator(regex=USERNAME_REGEX)
        ],
        max_length=150,
        required=True,
    )
    email = serializers.EmailField(
        validators=[
            UniqueValidator(queryset=CustomUser.objects.all())],
        max_length=254,
        required=True,
    )

    class Meta:
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')
        model = CustomUser
