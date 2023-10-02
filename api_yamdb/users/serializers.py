from django.core.validators import RegexValidator
from rest_framework import serializers
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainSerializer

from api.utils import Util
from users.models import CustomUser


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
                raise serializers.ValidationError('<me> can not be a username')
        return data


class UserRegistrationSerializer(CustomUserSerializer):
    """Сериализатор для модели пользователя."""

    class Meta:
        model = CustomUser
        fields = ('username', 'email')
    
    def create(self, validated_data):
        user = CustomUser(
            email=validated_data['email'],
            username=validated_data['username']
        )
        user.save()
        return user

    def create(self, validated_data):
        username = validated_data['username']
        email = validated_data['email']
        user = CustomUser.objects.create(username=username, email=email)
        Util.send_mail(validated_data['email'], user.confirmation_code)
        return user


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