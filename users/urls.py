from django.urls import path, reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from users.apps import UsersConfig
from users import views
from users.views import RegisterView, ProfileView, generate_new_password, verify_view, ResetUserPasswordView

app_name = UsersConfig.name

urlpatterns = [
    path('', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('confirm/<str:token>/', views.verify_view, name='verification'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/genpassword/', generate_new_password, name='generate_new_password'),
    path('verifying/', verify_view),
    path('password_reset/',
         ResetUserPasswordView.as_view(template_name="users/password_reset_form.html",
                                       success_url=reverse_lazy("users:login")),
         name='password_reset'),
]
