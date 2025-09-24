from django.urls import path
from . import views


urlpatterns = [
    path("", views.thread_list, name="chat_threads"),
    path("<int:pk>/", views.thread_detail, name="chat_thread_detail"),
]


