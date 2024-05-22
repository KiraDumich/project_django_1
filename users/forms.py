from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordResetForm

from users.models import User
from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from users.models import User


class StyleFormMixin():
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class RegistrationForm(StyleFormMixin, UserCreationForm):
    class Meta:
        model = User
        fields = ("email", "password1", "password2")


class RecoverForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = User
        fields = ("email",)


class UserForm(StyleFormMixin, UserChangeForm):
    class Meta:
        model = User
        fields = ("email", "password", "first_name", "last_name", "avatar", "phone", "country")

    def __int__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password"].widget = forms.HiddenInput()


class UserModerationForm(StyleFormMixin, UserChangeForm):
    class Meta:
        model = User
        fields = ("is_blocked",)


class UserRegisterForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')


class UserProfileForm(UserChangeForm):

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'phone', 'avatar')


class ChangeUserPasswordForm(StyleFormMixin, PasswordResetForm):
    pass