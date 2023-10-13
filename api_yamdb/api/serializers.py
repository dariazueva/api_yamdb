import re

from django.contrib.auth.tokens import default_token_generator
from django.core.validators import RegexValidator
from rest_framework import serializers, status
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainSerializer

from api.utils import send_code_to_mail
from reviews.models import Category, Comment, Genre, Review, Title, TitleGenre
from users.models import CustomUser

USERNAME_REGEX = r'^[\w.@+-]+$'


class UserRegistrationSerializer(serializers.Serializer):
    """Сериализатор для регистрации пользователя."""

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
        email = validated_data['email']
        username = validated_data['username']

        existing_user_by_email = CustomUser.objects.filter(email=email).first()

        if existing_user_by_email:
            if existing_user_by_email.username != username:
                raise serializers.ValidationError(
                    {'error': 'User with this email already exists '
                              'but with a different username.'},
                    code=status.HTTP_400_BAD_REQUEST
                )
            return existing_user_by_email

        existing_user_by_username = CustomUser.objects.filter(
            username=username).first()

        if existing_user_by_username:
            if existing_user_by_username.email != email:
                raise serializers.ValidationError(
                    {'error': 'User with this username already exists '
                              'but with a different email.'},
                    code=status.HTTP_400_BAD_REQUEST
                )
            return existing_user_by_username
        user = CustomUser.objects.create(email=email, username=username)
        confirmation_code = default_token_generator.make_token(user)
        send_code_to_mail(email, confirmation_code)
        return user

    def validate(self, data):
        username = data.get('username')

        if username:
            if username == 'me' or not re.match(USERNAME_REGEX, username):
                raise ValidationError('<me> can not be a username')
        return data


class CustomTokenObtainSerializer(TokenObtainSerializer):
    """Сериализатор для получения пользовательского токена."""

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
                code='invalid_confirmation_code',
            )
        self.user = user
        user.save()
        return {'token': str(self.get_token(self.user).access_token)}


class CustomUserSerializer(serializers.ModelSerializer):
    """Сериализатор для пользовательской модели."""

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


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для категорий."""

    name = serializers.CharField(
        max_length=256,
        validators=[
            UniqueValidator(queryset=Category.objects.all())],
    )
    slug = serializers.SlugField(
        max_length=50,
        validators=[
            UniqueValidator(queryset=Category.objects.all())],
    )

    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для жанров."""

    name = serializers.CharField(
        max_length=256,
        validators=[
            UniqueValidator(queryset=Genre.objects.all())],
    )
    slug = serializers.SlugField(
        max_length=50,
        validators=[
            UniqueValidator(queryset=Genre.objects.all())],
    )

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleGenreSerializer(serializers.ModelSerializer):
    """Сериализатор для связи между названием и жанром."""

    name = serializers.CharField()
    slug = serializers.CharField()

    class Meta:
        model = TitleGenre
        fields = ('name', 'slug')


class TitleReadSerializer(serializers.ModelSerializer):
    """Сериализатор для чтения информации о названии."""

    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(
        read_only=True,
        many=True
    )
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        fields = '__all__'
        model = Title


class TitleWriteSerializer(serializers.ModelSerializer):
    """Сериализатор для записи информации о названии."""

    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all())

    class Meta:
        fields = '__all__'
        model = Title


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для отзывов."""

    title = serializers.SlugRelatedField(
        slug_field='name',
        read_only=True
    )
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True

    )

    def validate_score(self, value):
        if value < 0 or value > 10:
            raise serializers.ValidationError(
                'Оценка должна быть в диапазоне от 0 до 10!')
        return value

    def validate(self, data):
        request = self.context['request']
        author = request.user
        title_id = self.context.get('view').kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        if (
                request.method == 'POST'
                and title.reviews.filter(author=author).exists()
        ):
            raise ValidationError('Может существовать только один отзыв!')
        return data

    class Meta:
        fields = '__all__'
        model = Review


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для комментариев."""

    review = serializers.SlugRelatedField(
        slug_field='text',
        read_only=True
    )
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        fields = ('id', 'author', 'review', 'text', 'pub_date')
        model = Comment
