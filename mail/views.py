from django.http import Http404
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from blog.models import Blog
from mail.forms import MailingForm, ClientForm, MessageForm, ManagerMailingForm
from mail.models import Mailing, Client, Message, Mail_Log


class MainView(TemplateView):
    template_name = 'mail/main_view.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data["mailing_count"] = Mailing.objects.all().count()  # количество рассылок всего
        context_data["active_mailing_count"] = Mailing.objects.filter(
            is_active=True,
        ).count()  # количество активных рассылок
        context_data["unique_clients_count"] = Client.objects.all().distinct().count()
        # количество уникальных клиентов для рассылок
        context_data["random_blogs"] = Blog.objects.order_by("?")[:3]  # три случайные статьи из блога
        return context_data


class MailingListView(LoginRequiredMixin, ListView):
    model = Mailing
    template_name = 'mail/mailing_list.html'

    def get_queryset(self):
        if self.request.user.has_perm('mailing.view_all_mailings'):
            mailing_list = super().get_queryset()
        else:
            mailing_list = super().get_queryset().filter(owner=self.request.user)
        return mailing_list

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(**kwargs)
        return context_data


class MailingDetailView(LoginRequiredMixin, DetailView):
    model = Mailing
    template_name = 'mail/mailing_detail.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        return context_data


class MailingCreateView(LoginRequiredMixin, CreateView):
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('mail:mailing_list')

    def form_valid(self, form):
        if form.is_valid():
            new_mail = form.save()
            new_mail.owner = self.request.user
            new_mail.save()

        return super().form_valid(form)


class MailingUpdateView(LoginRequiredMixin, UpdateView):
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('mail:mailing_list')

    def get_form_class(self):
        if self.request.user == self.object.owner or self.request.user.is_superuser:
            return MailingForm
        elif self.request.user.has_perm('mailing.set_deactivate'):
            return ManagerMailingForm
        else:
            raise Http404('У вас нет прав на редактирование рассылок')


class MailingDeleteView(LoginRequiredMixin, DeleteView):
    model = Mailing
    permission_required = 'main.delete_mailing'
    success_url = reverse_lazy('mail:mailing_list')

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        user = self.request.user
        if user.is_superuser:
            return self.object
        if user != self.object.owner:
            return Http404('Вы можете управлять только своей подпиской')

        return self.object


class ClientListView(LoginRequiredMixin, ListView):
    model = Client
    template_name = 'mail/client_list.html'


class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mail:client_list')

    def form_valid(self, form):
        if form.is_valid():
            new_client = form.save()
            new_client.owner = self.request.user
            new_client.save()

        return super().form_valid(form)


class ClientDeleteView(LoginRequiredMixin, DeleteView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mail:client_list')

    def get_object(self, queryset=None):
        user = self.request.user
        self.object = super().get_object(queryset)
        if user.is_superuser:
            return self.object
        if user != self.object.owner:
            return Http404('Вы можете управлять только своими получателями')

        return self.object


class ClientDetailView(LoginRequiredMixin, DetailView):
    model = Client
    template_name = 'mail/client_detail.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        return context_data


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mail:mailing_client')

    def get_object(self, queryset=None):
        user = self.request.user
        self.object = super().get_object(queryset)
        if user.is_superuser:
            return self.object
        if user != self.object.user:
            return Http404('Вы можете управлять только своими получателями')

        return self.object


class MessageListView(LoginRequiredMixin, ListView):
    model = Message
    template_name = 'mail/message_list.html'


class MessageDetailView(LoginRequiredMixin, DetailView):
    model = Message

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        return context_data


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('mail:message_list')

    def form_valid(self, form):
        if form.is_valid():
            new_message = form.save()
            new_message.owner = self.request.user
            new_message.save()

        return super().form_valid(form)


class MailLogView(LoginRequiredMixin, ListView):
    model = Mail_Log
    template_name = 'mail/logs.html'

    def get_queryset(self):
        """Метод для вывода логов только текущего пользователя"""
        return super().get_queryset().filter(user=self.request.user)

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(**kwargs)
        return context_data
