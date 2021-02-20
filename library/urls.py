from rest_framework import routers

from library.views import AuthorViewSet, BookViewSet


router = routers.DefaultRouter()
router.register('authors', AuthorViewSet, basename='author')
router.register('books', BookViewSet, basename='book')
urlpatterns = router.urls
