from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import (CustomUserViewSet, TokenObtainView,
                       UserRegistrationViewSet)
from .views import (CategoryViewSet, GenreViewSet, TitlesViewSet)

router_version1 = DefaultRouter()
router_version1.register('users', CustomUserViewSet, basename='user')
router_version1.register(r'categories', CategoryViewSet)
router_version1.register(r'genres', GenreViewSet)
router_version1.register(r'titles', TitlesViewSet)


urlpatterns = [
    path('', include(router_version1.urls)),
    path(
        'auth/signup/',
        UserRegistrationViewSet.as_view(
            {'post': 'create'}
        ),
        name='signup'
    ),
    path('auth/token/', TokenObtainView.as_view(), name='token_obtain'),
