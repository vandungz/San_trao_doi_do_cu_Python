from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render

from .models import Listing


def listings_list(request: HttpRequest) -> HttpResponse:
    items = Listing.objects.select_related("owner").order_by("-created_at")
    return render(request, "listings/list.html", {"items": items})


def listing_create(request: HttpRequest) -> HttpResponse:
    return render(request, "listings/create.html")


def listing_detail(request: HttpRequest, pk: int) -> HttpResponse:
    listing = get_object_or_404(Listing.objects.select_related("owner"), pk=pk)
    return render(request, "listings/detail.html", {"listing": listing})
