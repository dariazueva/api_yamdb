from rest_framework import serializers
from reviews.models import Category, Genre, Title, Review, Comment, TitleGenre
from django.db.models import Avg
import datetime as dt


class CategorySerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=256)
    slug = serializers.SlugField(max_length=50)

    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=256)
    slug = serializers.SlugField(max_length=50)

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleGenreSerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    slug = serializers.CharField()

    class Meta:
        model = TitleGenre
        fields = ('name', 'slug')


class TitleReadSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True)
    category = CategorySerializer()
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'rating',
                  'description', 'genre', 'category')

    def get_rating(self, obj):
        reviews = obj.review_set.all()
        average_score = reviews.aggregate(Avg('score'))['score__avg']
        return round(average_score) if average_score is not None else 0


class TitleWriteSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        many=True,
        slug_field='slug',
        queryset=Genre.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'rating',
                  'description', 'genre', 'category')

    def get_rating(self, obj):
        reviews = obj.review_set.all()
        average_score = reviews.aggregate(Avg('score'))['score__avg']
        return round(average_score) if average_score is not None else 0

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['genre'] = GenreSerializer(
            instance.genre.all(),
            many=True
        ).data
        representation['category'] = CategorySerializer(instance.category).data
        return representation

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
