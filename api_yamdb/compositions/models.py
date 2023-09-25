from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=256, verbose_name='Категория')
    slug = models.CharField(max_length=50, verbose_name='Слаг')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self) -> str:
        return self.name


class Genres(models.Model):
    name = models.CharField(max_length=256, verbose_name='Жанр')
    slug = models.CharField(max_length=50, verbose_name='Слаг')

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Titles(models.Model):
    name = models.CharField(max_length=256, verbose_name='Произведение')
    year = models.IntegerField(verbose_name='Год произведения')
    genre = models.ForeignKey(
        Genres,
        on_delete=models.SET_NULL,
        related_name='titles_genre',
        null=True
    )
    rating = models.IntegerField(verbose_name='Рэйтинг', default=0)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='titles_categories',
        null=True
    )
    description = models.TextField('Описание произведения', blank=True)

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self) -> str:
        return self.name


class Reviews(models.Model):
    text = models.TextField('Текст отзыва')
    score = models.IntegerField('Оценка произведения', default=0)

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'


class Comments(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments'
    )
    text = models.TextField('Текст комментария')
    pub_date = models.DateTimeField(
        'Дата добавления',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
