from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Category(models.Model):
    """Модель 'Категория'."""

    name = models.CharField(
        max_length=256,
        verbose_name='Категория',

    )
    slug = models.SlugField(
        max_length=50,
        verbose_name='Слаг',

    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self) -> str:
        return self.name


class Genre(models.Model):
    """Модель 'Жанр'."""

    name = models.CharField(
        max_length=256,
        verbose_name='Жанр',
        unique=True
    )
    slug = models.SlugField(
        max_length=50,
        verbose_name='Слаг',
        unique=True
    )

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self) -> str:
        return self.name


class Title(models.Model):
    """Модель 'Произведение'."""

    name = models.CharField(max_length=256,
                            verbose_name='Произведение',
                            help_text='Укажите название произведения'
                            )
    year = models.IntegerField(
        verbose_name='Год произведения',
        help_text='Укажите год произведения'
    )
    genre = models.ManyToManyField(
        Genre,
        through='TitleGenre',
        verbose_name='Жанр'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='titles_categories',
        null=True,
        verbose_name='Категория',
        unique=False,
        help_text='Укажите категорию произведения'
    )
    description = models.TextField(
        'Описание произведения',
        blank=True,
        help_text='Добавьте описание произведения'
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self) -> str:
        return self.name


class TitleGenre(models.Model):
    """Модель 'Произведение - Жанр'."""

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
    """Модель 'Отзыв'."""

    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews')
    author = models.ForeignKey(
        User, on_delete=models.CASCADE)
    text = models.TextField('Текст отзыва')
    score = models.IntegerField('Оценка произведения')
    pub_date = models.DateTimeField(
        'Дата добавления',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_title_author'
            )
        ]


class Comment(models.Model):
    """Модель 'Комментарий'."""

    author = models.ForeignKey(
        User, on_delete=models.CASCADE
    )
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField('Текст комментария')
    pub_date = models.DateTimeField(
        'Дата добавления',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
