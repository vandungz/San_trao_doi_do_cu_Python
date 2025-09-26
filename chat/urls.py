from django.urls import path

from . import views

app_name = "chat"

urlpatterns = [
    path("", views.threads_view, name="threads"),
    path("<int:pk>/", views.thread_detail_view, name="thread_detail"),
    path("<int:pk>/send/", views.post_message_view, name="thread_send"),
    path(
        "start/<int:listing_id>/<int:other_user_id>/",
        views.start_conversation_view,
        name="start_conversation",
    ),
    path("<int:pk>/poll/", views.poll_messages_view, name="thread_poll"),
]
