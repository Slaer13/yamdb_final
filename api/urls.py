from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CategoriesViewSet, CommentsViewSet, GenresViewSet,
                    ReviewsViewSet, TitlesViewset, UserViewSet, get_token,
                    send_code)

router = DefaultRouter()
router.register(r'titles/(?P<title_id>\d+)/reviews', ReviewsViewSet,
                basename='ReviewsViewSet')
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentsViewSet, basename='CommentsViewSet')
router.register(r'titles', TitlesViewset, basename='titles')
router.register(r'categories', CategoriesViewSet, basename='categories')
router.register(r'genres', GenresViewSet, basename='genres')
router.register('users', UserViewSet, basename='user')

urlpatterns = [
    path('v1/auth/email/', send_code),
    path('v1/auth/token/', get_token),
    path('v1/', include(router.urls)),
]
