from __future__ import annotations

from typing import Optional

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage, Paginator
from django.db.models import Max, Prefetch
from django.http import (
    Http404,
    HttpRequest,
    HttpResponse,
    HttpResponseForbidden,
    HttpResponseNotAllowed,
    JsonResponse,
)
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.utils.dateparse import parse_datetime

from listings.models import Listing

from .forms import MessageForm
from .models import Conversation, Message
from .services import (
    RateLimitError,
    create_message,
    get_or_create_conversation,
    mark_read,
    unread_count_by_conversation,
)


def _is_htmx(request: HttpRequest) -> bool:
    return request.headers.get("HX-Request") == "true"


def _wants_json(request: HttpRequest) -> bool:
    accept = request.headers.get("Accept", "")
    return "application/json" in accept or request.GET.get("format") == "json"


def _parse_after_param(after_param: Optional[str]):
    if not after_param:
        return None
    dt = parse_datetime(after_param)
    if dt is None:
        raise ValueError("Invalid timestamp format.")
    if timezone.is_naive(dt):
        dt = timezone.make_aware(dt, timezone=timezone.utc)
    return dt


def _prefetch_last_message(qs):
    return qs.prefetch_related(
        Prefetch(
            "messages",
            queryset=Message.objects.select_related("sender").order_by("-created_at"),
            to_attr="_last_messages",
        )
    )


def _get_messages_page(conversation: Conversation, page_number: Optional[str]):
    qs = conversation.messages.select_related("sender").order_by("created_at")
    paginator = Paginator(qs, 25)
    if not page_number:
        page_number = paginator.num_pages or 1
    try:
        page = paginator.page(page_number)
    except EmptyPage:
        page = paginator.page(paginator.num_pages or 1)
    return page


@login_required
def threads_view(request: HttpRequest) -> HttpResponse:
    conversations_qs = (
        Conversation.objects.for_user(request.user)
        .select_related("listing", "buyer", "seller")
        .annotate(last_message_at=Max("messages__created_at"))
        .order_by("-last_message_at", "-created_at")
    )
    conversations_qs = _prefetch_last_message(conversations_qs)

    paginator = Paginator(conversations_qs, 20)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    unread_map = unread_count_by_conversation(request.user)

    conversations = list(page_obj.object_list)
    for convo in conversations:
        convo.other_user = convo.other_participant(request.user)
        convo.unread_total = unread_map.get(convo.pk, 0)
        convo.last_message_obj = convo.last_message
        convo.last_activity_at = (
            convo.last_message_obj.created_at if convo.last_message_obj else convo.created_at
        )

    context = {
        "page_obj": page_obj,
        "conversations": conversations,
    }
    return render(request, "chat/threads.html", context)


@login_required
def thread_detail_view(request: HttpRequest, pk: int) -> HttpResponse:
    conversation = get_object_or_404(
        Conversation.objects.select_related("listing", "buyer", "seller"),
        pk=pk,
    )
    if not conversation.is_participant(request.user):
        return HttpResponseForbidden("Ban khong co quyen truy cap cuoc tro chuyen nay.")

    partner = conversation.other_participant(request.user)
    page_number = request.GET.get("page")
    page_obj = _get_messages_page(conversation, page_number)

    mark_read(conversation, request.user)

    last_message_ts = ""
    if page_obj.object_list:
        last_created = page_obj.object_list[-1].created_at
        last_message_ts = timezone.localtime(last_created).isoformat()

    form = MessageForm()

    context = {
        "conversation": conversation,
        "partner": partner,
        "page_obj": page_obj,
        "messages": page_obj.object_list,
        "form": form,
        "last_message_ts": last_message_ts,
    }
    return render(request, "chat/thread_detail.html", context)


@login_required
def post_message_view(request: HttpRequest, pk: int) -> HttpResponse:
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])

    conversation = get_object_or_404(
        Conversation.objects.select_related("listing", "buyer", "seller"),
        pk=pk,
    )
    if not conversation.is_participant(request.user):
        return HttpResponseForbidden("Ban khong the gui tin trong cuoc tro chuyen nay.")

    form = MessageForm(request.POST)
    if form.is_valid():
        try:
            message = create_message(
                conversation=conversation,
                sender=request.user,
                body=form.cleaned_data["body"],
            )
        except RateLimitError as exc:
            form.add_error(None, str(exc))
        except ValueError as exc:
            form.add_error("body", str(exc))
        except PermissionError as exc:
            form.add_error(None, str(exc))
        else:
            last_ts = timezone.localtime(message.created_at).isoformat()
            if _is_htmx(request) or _wants_json(request):
                response = render(
                    request,
                    "chat/_message_list.html",
                    {
                        "messages": [message],
                        "conversation": conversation,
                    },
                )
                response.status_code = 201
                response["X-Last-Timestamp"] = last_ts
                return response
            return redirect("chat:thread_detail", pk=conversation.pk)

    if _is_htmx(request) or _wants_json(request):
        return JsonResponse({"errors": form.errors}, status=400)

    page_obj = _get_messages_page(conversation, request.GET.get("page"))
    partner = conversation.other_participant(request.user)
    context = {
        "conversation": conversation,
        "partner": partner,
        "page_obj": page_obj,
        "messages": page_obj.object_list,
        "form": form,
        "last_message_ts": "",
    }
    return render(request, "chat/thread_detail.html", context, status=400)


@login_required
def start_conversation_view(request: HttpRequest, listing_id: int, other_user_id: int) -> HttpResponse:
    listing = get_object_or_404(Listing.objects.select_related("owner"), pk=listing_id)
    user_model = get_user_model()
    other_user = get_object_or_404(user_model, pk=other_user_id)

    if request.user.pk == listing.owner_id:
        seller = listing.owner
        buyer = other_user
    else:
        seller = listing.owner
        buyer = request.user
        if other_user.pk != seller.pk:
            raise Http404("Nguoi dung khong phai chu tin.")

    if buyer.pk == seller.pk:
        raise Http404("Khong the tu nhan voi chinh minh.")

    conversation = get_or_create_conversation(
        listing_id=listing.pk,
        buyer_id=buyer.pk,
        seller_id=seller.pk,
    )
    return redirect("chat:thread_detail", pk=conversation.pk)


@login_required
def poll_messages_view(request: HttpRequest, pk: int) -> HttpResponse:
    conversation = get_object_or_404(
        Conversation.objects.select_related("listing", "buyer", "seller"),
        pk=pk,
    )
    if not conversation.is_participant(request.user):
        return HttpResponseForbidden("Ban khong the truy cap cuoc tro chuyen nay.")

    try:
        after_dt = _parse_after_param(request.GET.get("after"))
    except ValueError:
        return JsonResponse({"error": "Tham so thoi gian khong hop le."}, status=400)

    messages_qs = conversation.messages.select_related("sender").order_by("created_at")
    if after_dt:
        messages_qs = messages_qs.filter(created_at__gt=after_dt)

    new_messages = list(messages_qs)
    if not new_messages:
        if _is_htmx(request):
            response = render(
                request,
                "chat/_message_list.html",
                {"messages": [], "conversation": conversation},
            )
            response["X-Last-Timestamp"] = request.GET.get("after", "")
            return response
        return JsonResponse({"messages": [], "last_ts": request.GET.get("after", "")})

    mark_read(conversation, request.user)

    last_ts = timezone.localtime(new_messages[-1].created_at).isoformat()

    if _is_htmx(request):
        response = render(
            request,
            "chat/_message_list.html",
            {"messages": new_messages, "conversation": conversation},
        )
        response["X-Last-Timestamp"] = last_ts
        return response

    payload = [
        {
            "id": message.pk,
            "sender": message.sender_id,
            "sender_display": message.sender.get_full_name()
            or message.sender.get_username(),
            "is_self": message.sender_id == request.user.pk,
            "body": message.body,
            "created_at": timezone.localtime(message.created_at).isoformat(),
            "read_at": timezone.localtime(message.read_at).isoformat()
            if message.read_at
            else None,
        }
        for message in new_messages
    ]
    return JsonResponse({"messages": payload, "last_ts": last_ts})
