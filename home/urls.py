from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("register/", views.register, name="register"),
    path("login/", views.user_login, name="login"),
    path("logout/", auth_views.LogoutView.as_view(next_page="/"), name="logout"),
    path("settings/", views.user_settings, name="user_settings"),
    path("@<str:username>/", views.user_profile, name="user_profile"),
    path(
        "password_change/",
        views.CustomPasswordChangeView.as_view(),
        name="password_change",
    ),
    path(
        "password_change/done/", views.password_change_done, name="password_change_done"
    ),
    path("search/", views.search, name="search"),
    # APIs
    path("api/posts/", views.get_posts, name="get_posts"),
    path("api/posts/<int:post_id>/", views.delete_post, name="delete_post"),
    path("api/posts/<int:post_id>/like/", views.like_post, name="like_post"),
    path("api/posts/<int:post_id>/comments/", views.add_comment, name="add_comment"),
    path(
        "api/comments/<int:comment_id>/",
        views.delete_comment,
        name="delete_comment",
    ),
]

# Serving media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
