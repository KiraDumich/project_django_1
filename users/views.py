import secrets
import string
from random import random, randint

from config import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView, LoginView
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse  # reverse_lazy - для возвращения ссылки, на которую попадёт пользователь
from django.views.generic import CreateView, UpdateView

from users.forms import UserProfileForm, UserRegisterForm, ChangeUserPasswordForm  # кастомные модели
from users.models import User


class UserLoginView(LoginView):
    redirect_authenticated_user = True
    success_url = reverse_lazy('catalog:home')


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy('users:login')
    template_name = 'users/register.html'

    def form_valid(self, form):

        user = form.save()
        user.is_active = False
        verified_password = "".join([str(randint(1, 9)) for _ in range(10)])
        user.verified_password = verified_password
        user.save()
        current_site = self.request.get_host()
        verified_link = f'http://{current_site}/users/confirm/{verified_password}/'
        send_mail(
            subject='Верификация почты',
            message=f'Если вы регистрировались в Skystore: нажмите на ссылку: '
                    f'{verified_link}\n Так вы подтвердите почту',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
            fail_silently=False
        )

        return super().form_valid(form)


def verify_view(request, token):  # Функция для верификации
    user = User.objects.filter(verified_password=token)
    if user:
        user.is_active = True
        user.save()
    return redirect('users:login')


class ProfileView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user


def generate_new_password(request):
    new_password = ''.join([str(random.randint(0, 9)) for _ in range(12)])
    send_mail(
        subject='Вы сменили пароль',
        message=f'Ваш новый пароль: {new_password}',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[request.user.email]
    )
    request.user.set_password(new_password)
    request.user.save()
    return redirect(reverse('catalog:home'))


class ResetUserPasswordView(PasswordResetView):  # Контроллер для восстановления пароля
    form_class = ChangeUserPasswordForm
    success_url = reverse_lazy('users:login')

    # def get_object(self, queryset=None):
    #     return self.request.user

    # def get_success_url(self):
    #     return reverse_lazy('users:login')

    def form_valid(self, form):
        if self.request.method == 'POST':
            email = self.request.POST['email']
            try:
                user = User.objects.get(email=email)
                alphabet = string.ascii_letters + string.digits
                password = "".join(secrets.choice(alphabet) for i in range(10))
                user.set_password(password)
                user.save()
                message = f"Ваш новый пароль:\n{password}"
                send_mail(
                    "Смена пароля",
                    message=message,
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[user.email],
                    fail_silently=False,
                )
            except User.DoesNotExist:
                return render(self.request, 'users/password_reset_form.html',
                              {'error_message': 'Пользователь с таким email не найден'})
        return super().form_valid(form)


class UserPasswordResetConfirmView(PasswordResetConfirmView):
    pass
