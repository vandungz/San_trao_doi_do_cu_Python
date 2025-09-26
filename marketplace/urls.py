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
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", TemplateView.as_view(template_name="home.html"), name="home"),
    path("accounts/", include("accounts.urls")),
     path('listings/', include(('listings.urls', 'listings'), namespace='listings')),
    path("chat/", include("chat.urls")),
     
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
