from rest_framework import serializers, validators
from reviews.models import Category, Genre, Title, Review, Comment, GenreTitle
import datetime as dt

CHOICES = [rating for rating in range(11)]


class CategorySerializer(serializers.ModelSerializer):
    name = serializers.CharField(
        max_length=256,
        validators=[validators.UniqueValidator(
            queryset=Category.objects.all())])
    slug = serializers.SlugField(
        max_length=50,
        validators=[validators.UniqueValidator(
            queryset=Category.objects.all())]
    )

    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    name = serializers.CharField(
        max_length=256,
        validators=[validators.UniqueValidator(
            queryset=Genre.objects.all())])
    slug = serializers.SlugField(
        max_length=50,
        validators=[validators.UniqueValidator(
            queryset=Genre.objects.all())]
    )

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class GenreTitleSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='genre.name')
    slug = serializers.CharField(source='genre.slug')

    class Meta:
        model = GenreTitle
        fields = ('name', 'slug')


class TitleSerializer(serializers.ModelSerializer):
    genre = GenreTitleSerializer(many=True,)
    category = CategorySerializer()

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'rating',
                  'description', 'genre', 'category')        

    def validate_year(self, value):
        year = dt.date.today().year
        if (year < value):
            raise serializers.ValidationError(
                'Год выпуска не может быть больше текущего')
        return value

    def validate_rating(self, value):
        if value < 0 or value > 10:
            raise serializers.ValidationError('Рэйтинг должен быть от 0 до 10')
        return value


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
