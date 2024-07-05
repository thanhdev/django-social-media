from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("register/", views.register, name="register"),
    path("login/", views.user_login, name="login"),
    # APIs
    path("api/posts/", views.get_posts, name="get_posts"),
    path("api/posts/<int:post_id>/delete/", views.delete_post, name="delete_post"),
    path("api/posts/<int:post_id>/like/", views.like_post, name="like_post"),
]

# Serving media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
