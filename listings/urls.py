from django.urls import path
from . import views


urlpatterns = [
    path("", views.listings_list, name="listings_list"),
    path("create/", views.listing_create, name="listing_create"),
    path("<int:pk>/", views.listing_detail, name="listing_detail"),
]


