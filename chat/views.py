from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def thread_list(request: HttpRequest) -> HttpResponse:
    return render(request, "chat/threads.html", {"threads": []})


def thread_detail(request: HttpRequest, pk: int) -> HttpResponse:
    return render(request, "chat/thread_detail.html", {"pk": pk})


