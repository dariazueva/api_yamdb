from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import (CategoryViewSet, CommentViewSet, CustomUserViewSet,
                       GenreViewSet, ReviewViewSet, TitlesViewSet,
                       TokenObtainView, UserRegistrationViewSet)

router_version1 = DefaultRouter()
router_version1.register(
    'users',
    CustomUserViewSet,
    basename='user')
router_version1.register(
    r'categories',
    CategoryViewSet)
router_version1.register(
    r'genres',
    GenreViewSet)
router_version1.register(
    'titles',
    TitlesViewSet,
    basename='titles'
)
router_version1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)
router_version1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)

auth_urls = [
    path(
        'signup/',
        UserRegistrationViewSet.as_view(
            {'post': 'create'}
        ),
        name='signup'
    ),
    path('token/', TokenObtainView.as_view(), name='token_obtain'),
]

urlpatterns = [
    path('', include(router_version1.urls)),
    path('auth/', include(auth_urls)), ]
