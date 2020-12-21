
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    # Accounts
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),

    # Posts
    path('profile/<int:id>', views.profile, name='profile'),
    path("followed_posts", views.followed_posts, name='f_posts'),

    
    # JS API
    path('like/check/<int:id>', views.get_like_info, name='like_info'),
    path("toggle_like/<int:id>", views.toggle_like, name='toggle_like'),
    path('edit/<int:id>', views.edit, name='edit'),
    path("posts/create", views.make_post, name='create_post'),
    path("follow/<int:id>", views.toggle_follow, name='follow'),
]
