from . import views
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("following", views.following, name="following"),

    path("accounts/", include('django.contrib.auth.urls')),
    path("accounts/register/", views.UserCreationView.as_view(), name='register'),

    #path("login", views.login_view, name="login"),
    #path("logout", views.logout_view, name="logout"),
    #path("register", views.register, name="register"),
    path('accounts/profile/', views.edit_profile, name='profile'),
    path("profile/<int:pk>", views.ProfileDetailView.as_view(), name="profile_detail"),
    path("follow_unfollow/", views.follow_unfollow, name="switch"),

    #API Routes
    path("posts/", views.posts, name="posts"),
    path("posts/<int:post_id>", views.likes, name="likes"),
    path("posts/msg/<int:post_id>", views.edit_msg, name="msg"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
