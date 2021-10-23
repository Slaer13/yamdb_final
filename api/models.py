from django.contrib.auth.models import AbstractUser
from django.core import validators as vl
from django.db import models
from django.utils.translation import gettext_lazy as _

from .validators import custom_year_validator


class CustomUser(AbstractUser):

    class PermissionsRoleChoice(models.TextChoices):
        USER = 'user', _('user')
        MODERATOR = 'moderator', _('moderator')
        ADMIN = 'admin', _('admin')

    bio = models.TextField(blank=True, null=True)
    email = models.EmailField(_('email address'), unique=True)
    role = models.CharField(
        max_length=50,
        choices=PermissionsRoleChoice.choices,
        default=PermissionsRoleChoice.USER
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email


class Category(models.Model):
    name = models.CharField(
        max_length=200,
        unique=True,
        db_index=True,
        verbose_name='Название категории'
    )
    slug = models.SlugField(
        max_length=300,
        unique=True,
        verbose_name='Метка категории'
    )

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ('name',)


class Genre(models.Model):
    name = models.CharField(
        max_length=200,
        unique=True,
        db_index=True,
        verbose_name='Название жанра'
    )
    slug = models.SlugField(
        max_length=300,
        unique=True,
        verbose_name='Метка жанра'
    )

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ('name',)


class Title(models.Model):
    name = models.CharField(
        max_length=200,
        unique=True,
        db_index=True,
        verbose_name='Название'
    )
    year = models.IntegerField(
        null=True,
        verbose_name='Год',
        validators=[
            custom_year_validator,
        ]
    )
    description = models.TextField(
        null=True,
        verbose_name='Описание произведения'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='titles',
        verbose_name='Категория'
    )
    genre = models.ManyToManyField(
        Genre,
        blank=True,
        related_name='titles',
        verbose_name='Жанр'
    )

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'


class Review(models.Model):
    text = models.TextField(verbose_name='Текст')
    score = models.IntegerField(
        verbose_name='Оценка',
        validators=[
            vl.MinValueValidator(1, message='Введите число не меньше 1'),
            vl.MaxValueValidator(10, message='Введите число не больше 10')
        ]
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации'
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        db_index=True,
        related_name='reviews',
        verbose_name='Произведение'
    )
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор'
    )

    def __str__(self) -> str:
        return (f'{self.author} написал {self.text} на {self.title}.'
                f'{self.author} оценил {self.title} на {self.score}.'
                f'{self.pub_date}.')

    class Meta:
        verbose_name = 'Рецензия'
        verbose_name_plural = 'Рецензии'
        ordering = ('-pub_date', 'author',)


class Comment(models.Model):
    text = models.TextField(verbose_name='Текст')
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации'
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        db_index=True,
        related_name='comments',
        blank=True,
        null=True,
        verbose_name='Рецензия'
    )
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор'
    )

    def __str__(self) -> str:
        return (f'{self.author} написал {self.text} на {self.review}.'
                f'{self.pub_date}.')

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('-pub_date', 'author',)
