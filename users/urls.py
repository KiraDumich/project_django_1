from django.urls import path, reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from users.apps import UsersConfig
from users.views import (RegisterView, verify, rebuild_access, UserDetailView, UserProfileView, UserListView,
                         UserModerationView)

app_name = UsersConfig.name

urlpatterns = [
    path("", LoginView.as_view(template_name="users/login.html"), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("registration/", RegisterView.as_view(), name="register"),
    path("verify/<str:token>", verify, name="verify"),
    path("restore_access/", rebuild_access, name="rebuild"),
    path("<int:pk>/view/", UserDetailView.as_view(), name="user_detail"),
    path("user_update/", UserProfileView.as_view(), name="user_profile"),
    path("user_list/", UserListView.as_view(), name="user_list"),
    path("user_moderation/<int:pk>/", UserModerationView.as_view(), name="user_moderator"),
]
