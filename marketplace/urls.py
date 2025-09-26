# from django.urls import path
# # from . import views


# urlpatterns = [
#     path("", views.thread_list, name="chat_threads"),
#     path("<int:pk>/", views.thread_detail, name="chat_thread_detail"),
# ]

# from django.contrib import admin
# from django.urls import path, include

# urlpatterns = [
#     path("admin/", admin.site.urls),
#     path("accounts/", include("accounts.urls")),
#     path("listings/", include("listings.urls")),
#     path("chat/", include("chat.urls")),
#     path("", include("listings.urls")),  # Trang chủ tạm thời trỏ về listings
# ]


from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls")),   # nếu có app accounts
    path("listings/", include("listings.urls")),   # <-- phải có dòng này
    path("chat/", include("chat.urls")),
    path("", include("listings.urls")),  # Trang chủ tạm trỏ về listings
]
