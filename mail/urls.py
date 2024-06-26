from django.urls import path
from django.views.decorators.cache import cache_page

from mail.apps import MailConfig
from mail.views import (ClientCreateView, ClientDeleteView, ClientListView,
                        ClientUpdateView, MailingCreateView, MailingDeleteView,
                        MailingDetailView, MailingListView, MailingUpdateView,
                        MessageCreateView, MessageListView, ClientDetailView, MainView, MailLogView)


app_name = MailConfig.name


urlpatterns = [
    path('', MainView.as_view(), name='main_view'),
    path("mailingdetails/<int:pk>/", MailingDetailView.as_view(), name="mailing_detail"),
    path("mailingcreate/", MailingCreateView.as_view(), name="mailing_create"),
    path("mailingupdate/<int:pk>/", MailingUpdateView.as_view(), name="mailing_update"),
    path("mailingdelete/<int:pk>/", MailingDeleteView.as_view(), name="mailing_delete"),
    path("messagelist/", MessageListView.as_view(), name="message_list"),
    path("messagecreate/", MessageCreateView.as_view(), name="message_create"),
    path("clientlist/", ClientListView.as_view(), name="client_list"),
    path("clientcreate/", ClientCreateView.as_view(), name="client_create"),
    path("clientdetails/<int:pk>/", ClientDetailView.as_view(), name="client_detail"),
    path("clientupdate<int:pk>/", ClientUpdateView.as_view(), name="client_update"),
    path("clientdelete/<int:pk>/", ClientDeleteView.as_view(), name="client_delete"),
    path("maillist", MailingListView.as_view(), name="mailing_list"),
    path('mailing/logs_list/', MailLogView.as_view(), name='logs_list'),
]