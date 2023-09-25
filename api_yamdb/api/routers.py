from rest_framework.routers import DefaultRouter

from .views import CategoryViewSet, GenreViewSet, TitlesViewSet, ReviewViewSet, CommentViewSet

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'titles', TitlesViewSet)
router.register(r'genres', GenreViewSet)
router.register(
    r'^titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
router.register(
    r'^titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)
