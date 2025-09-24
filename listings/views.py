from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def listings_list(request: HttpRequest) -> HttpResponse:
    return render(request, "listings/list.html", {"items": []})


def listing_create(request: HttpRequest) -> HttpResponse:
    return render(request, "listings/create.html")


def listing_detail(request: HttpRequest, pk: int) -> HttpResponse:
    return render(request, "listings/detail.html", {"pk": pk})


