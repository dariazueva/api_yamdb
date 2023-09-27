from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Category(models.Model):
    name = models.CharField(
        max_length=256, verbose_name='Категория', unique=True)
    slug = models.CharField(max_length=50, verbose_name='Слаг', unique=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self) -> str:
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=256, verbose_name='Жанр', unique=True)
    slug = models.CharField(max_length=50, verbose_name='Слаг', unique=True)

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self) -> str:
        return self.name


class Title(models.Model):
    name = models.CharField(max_length=256, verbose_name='Произведение')
    year = models.IntegerField(verbose_name='Год произведения')
    genre = models.ManyToManyField(
        Genre,
        through='TitleGenre',
        verbose_name='Жанр'
    )
    rating = models.IntegerField(verbose_name='Рэйтинг', default=0)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='titles_categories',
        null=True,
        verbose_name='Категория',
        unique=False
    )
    description = models.TextField('Описание произведения', blank=True)

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self) -> str:
        return self.name


class TitleGenre(models.Model):
    title_id = models.ForeignKey(
        Title, on_delete=models.CASCADE,
        null=True,
        verbose_name='Название произведения')
    genre_id = models.ForeignKey(
        Genre, on_delete=models.CASCADE,
        null=True,
        verbose_name='Жанр произведения')

    class Meta:
        verbose_name = 'Произведение - Жанр'
        verbose_name_plural = 'Произведение - Жанр'

    def __str__(self):
        return f'{self.title_id} - {self.genre_id}'


class Review(models.Model):
    title = models.ForeignKey(Title, on_delete=models.CASCADE)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE)
    text = models.TextField('Текст отзыва')
    score = models.IntegerField('Оценка произведения', default=0)
    pub_date = models.DateTimeField(
        'Дата добавления',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments'
    )
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    text = models.TextField('Текст комментария')
    pub_date = models.DateTimeField(
        'Дата добавления',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
