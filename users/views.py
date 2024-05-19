import secrets
import string
from random import random, randint
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import Http404

from config import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView, LoginView
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse  # reverse_lazy - для возвращения ссылки, на которую попадёт пользователь
from django.views.generic import CreateView, UpdateView, ListView, DetailView

from users.forms import RegistrationForm, RecoverForm, UserForm, UserModerationForm  # кастомные модели
from users.models import User


class RegisterView(CreateView):
    model = User
    form_class = RegistrationForm

    def get_success_url(self):
        return reverse("users:login")

    def form_valid(self, form):
        user = form.save()
        token = secrets.token_hex(16)
        user.token = token
        user.is_active = False
        user.save()
        host = self.request.get_host()
        url = f"http://{host}/users/verify/{token}"
        message = f"Для подтверждения почты Вам нужно перейти по ссылке: {url}"
        send_mail("Верификация почты", message, settings.EMAIL_HOST_USER, [user.email])
        return super().form_valid(form)


def verify(request, token):
    user = get_object_or_404(User, token=token)
    user.verified = True
    user.is_active = True
    user.save()
    return redirect(reverse("users:login"))


def rebuild_access(request):
    if request.method == "POST":
        email = request.POST.get("email")
        user = User.objects.get(email=email)
        new_password = "".join([str(randint(0, 9)) for _ in range(8)])

        message = f"Ваш новый пароль : {new_password}"
        send_mail(
            "Восстановление доступа", message, settings.EMAIL_HOST_USER, [user.email]
        )
        user.set_password(new_password)
        user.save()
        return redirect(reverse("users:login"))
    else:
        form = RecoverForm
        context = {"form": form}
        return render(request, "users/password_reset_form.html", context)


class UserListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = User
    template_name = 'users/user_list.html'
    permission_required = ('users.view_user',)

    def get_queryset(self):
        customer_list = super().get_queryset()
        user = self.request.user
        if user.is_blocked:
            raise Http404("Вы заблокированы менеджером")
        else:
            return customer_list


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'users/user_detail.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        return context_data


class UserProfileView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'users/user_formprofile.html'
    form_class = UserForm
    success_url = reverse_lazy("users:user_list")

    def get_object(self, queryset=None):
        return self.request.user


class UserModerationView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = User
    form_class = UserModerationForm
    template_name = 'users/block_user.html'
    permission_required = ('users.block_users',)

    def get_success_url(self):
        return reverse_lazy('users:user_list')
