from django.core import validators as vl
from django.shortcuts import get_object_or_404
from rest_framework import serializers, validators

from .models import Category, Comment, CustomUser, Genre, Review, Title
from .validators import custom_year_validator


class EmailSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()

    class Meta:
        fields = ['email']
        model = CustomUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['first_name', 'last_name', 'username', 'bio',
                  'email', 'role']
        model = CustomUser


class TitleToReviewDefault:
    requires_context = True

    def __call__(self, serializer_field):
        title_id = serializer_field.context.get('view').kwargs.get('title_id')
        # title = get_object_or_404(Title, id=title_id)
        # return title
        return get_object_or_404(Title, id=title_id)


class ReviewSerializer(serializers.ModelSerializer):
    title = serializers.SlugRelatedField(
        slug_field='name',
        write_only=True,
        queryset=Title.objects.all(),
        default=TitleToReviewDefault()
    )
    author = serializers.SlugRelatedField(
        slug_field='username',
        queryset=CustomUser.objects.all(),
        default=serializers.CurrentUserDefault()
    )
    score = serializers.IntegerField(
        validators=(
            vl.MinValueValidator(1, message='Введите число не меньше 1'),
            vl.MaxValueValidator(10, message='Введите число не больше 10'),
        )
    )

    class Meta:
        fields = '__all__'
        model = Review
        validators = [
            validators.UniqueTogetherValidator(
                queryset=Review.objects.all(),
                fields=['author', 'title'],
                message='Вы уже оставляли отзыв на это произведение'
            )
        ]


class CommentSerializer(serializers.ModelSerializer):
    text = serializers.CharField()
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        fields = '__all__'
        model = Comment


class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        exclude = ('id',)
        model = Category


class GenresSerializer(serializers.ModelSerializer):
    class Meta:
        exclude = ('id',)
        model = Genre


class TitleSerializer(serializers.ModelSerializer):
    rating = serializers.FloatField(read_only=True)

    class Meta:
        model = Title
        fields = '__all__'


class TitlesSerializerGet(TitleSerializer):
    genre = GenresSerializer(many=True)
    category = CategoriesSerializer()


class TitlesSerializerPost(TitleSerializer):
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all(),
        required=False
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True
    )
    year = serializers.IntegerField(
        required=False,
        validators=(custom_year_validator,)
    )
