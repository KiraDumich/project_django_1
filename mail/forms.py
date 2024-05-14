from django import forms

from mail.models import Client, Mailing, Message


class MailingForm(forms.ModelForm):
    class Meta:
        model = Mailing
        fields = "__all__"


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = "__all__"


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = "__all__"


class ManagerMailingForm(MailingForm):
    """
    Класс для создания формы рассылки для менеджера
    """

    class Meta:
        model = Mailing
        fields = ('mailing_status',)