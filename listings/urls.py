from django.urls import path
from . import views

urlpatterns = [
    path("", views.ListingListView.as_view(), name="list"),
    path("mine/", views.my_listings, name="mine"),
    path("create/", views.ListingCreateView.as_view(), name="create"),
    path("<int:pk>/", views.ListingDetailView.as_view(), name="detail"),  # 👈 dùng pk thôi
    path("<int:pk>/edit/", views.ListingUpdateView.as_view(), name="edit"),
    path("<int:pk>/delete/", views.ListingDeleteView.as_view(), name="delete"),
    path("<int:pk>/publish/", views.publish_listing, name="publish"),
      # ✅ Route xóa ảnh riêng lẻ
    path('image/<int:image_id>/delete/', views.delete_image, name='delete_image'),
]
