from rest_framework import serializers, validators
from reviews.models import Category, Genre, Title, Review, Comment, TitleGenre
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


class TitleSerializer(serializers.ModelSerializer):
    genre = TitleGenreSerializer(many=True)
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

    def create(self, validated_data):
        genre_data = validated_data.pop('genre', [])
        category_data = validated_data.pop('category', None)

        title = Title.objects.create(**validated_data)

        for genre_item in genre_data:
            genre, created = Genre.objects.get_or_create(
                name=genre_item['name'],
                slug=genre_item['slug']
            )
            title.genre.add(genre)

        if category_data:
            category, created = Category.objects.get_or_create(
                name=category_data['name'],
                slug=category_data['slug']
            )
            title.category = category

        title.save()
        return title

    def update(self, instance, validated_data):
        genre_data = validated_data.pop('genre', [])
        category_data = validated_data.pop('category', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.genre.clear()
        for genre_item in genre_data:
            genre, created = Genre.objects.get_or_create(
                name=genre_item['name'],
                slug=genre_item['slug']
            )
            instance.genre.add(genre)

        if category_data:
            category, created = Category.objects.get_or_create(
                name=category_data['name'],
                slug=category_data['slug']
            )
            instance.category = category

        instance.save()
        return instance


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
