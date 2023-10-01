from django.core.validators import RegexValidator
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainSerializer

from users.models import CustomUser


from django.contrib.auth import authenticate


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

    # def validate(self, data):
    #     email = data.get('email', None)
    #     username = data.get('username', None)
    #     if email is None:
    #         raise serializers.ValidationError(
    #             'An email address is required to log in.'
    #         )
    #     if username is None:
    #         raise serializers.ValidationError(
    #             'A username is required to log in.'
    #         )
    #     user = authenticate(email=email, username=username)
        # if user is None:
        #     raise serializers.ValidationError(
        #         'A user with this email and username was not found.'
        #     )

        # # Django предоставляет флаг is_active для модели User. Его цель
        # # сообщить, был ли пользователь деактивирован или заблокирован.
        # # Проверить стоит, вызвать исключение в случае True.
        # if not user.is_active:
        #     raise serializers.ValidationError(
        #         'This user has been deactivated.'
        #     )

        # return {
        #     'email': user.email,
        #     'username': user.username
        # }


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

