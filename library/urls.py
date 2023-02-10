from django.conf.urls import include
from django.urls import path, re_path
from rest_framework.routers import DefaultRouter
from library import views


router = DefaultRouter(trailing_slash=False)

router.register(r'books', views.BooksViewSet)
router.register(r'author', views.AuthorViewSet)

urlpatterns = [
    re_path('v1/', include(router.urls)),
    path('create/', views.CreateUserView.as_view(), name='create'),
    path('token/', views.CreateTokenView.as_view(), name='token'),
]


