from __future__ import annotations

from typing import Dict

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.core.mail import EmailMultiAlternatives
from django.db import transaction
from django.db.models import Count
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils import timezone
from django.utils.html import strip_tags
from django.utils.text import Truncator

from listings.models import Listing

from .models import Conversation, Message

RATE_LIMIT_SECONDS = 2
EMAIL_DEBOUNCE_SECONDS = 60
DEFAULT_FROM_EMAIL = getattr(settings, "DEFAULT_FROM_EMAIL", "no-reply@marketplace.local")


class RateLimitError(Exception):
    """Raised when the user hits the chat send rate limit."""


def get_or_create_conversation(listing_id: int, buyer_id: int, seller_id: int) -> Conversation:
    listing = Listing.objects.select_related("owner").get(pk=listing_id)
    user_model = get_user_model()
    buyer = user_model.objects.get(pk=buyer_id)
    seller = user_model.objects.get(pk=seller_id)

    if listing.owner_id != seller_id:
        raise ValueError("Seller must be the owner of the listing.")
    if buyer_id == seller_id:
        raise ValueError("Buyer and seller must be different users.")

    with transaction.atomic():
        conversation, _created = (
            Conversation.objects.select_for_update()
            .get_or_create(listing=listing, buyer=buyer, seller=seller)
        )
    return conversation


def create_message(conversation: Conversation, sender, body: str) -> Message:
    if not conversation.is_participant(sender):
        raise PermissionError("Sender is not allowed in this conversation.")

    trimmed_body = body.strip()
    if not trimmed_body:
        raise ValueError("Message body cannot be empty.")

    rate_key = f"chat:rate:{sender.pk}"
    if not cache.add(rate_key, timezone.now().isoformat(), RATE_LIMIT_SECONDS):
        raise RateLimitError("Ban dang gui tin nhan qua nhanh. Thu lai sau giay lat.")

    message = Message.objects.create(
        conversation=conversation,
        sender=sender,
        body=trimmed_body,
    )

    _maybe_send_new_message_email(message)
    return message


def mark_read(conversation: Conversation, user) -> int:
    if not conversation.is_participant(user):
        return 0
    return (
        Message.objects.filter(
            conversation=conversation,
            read_at__isnull=True,
        )
        .exclude(sender=user)
        .update(read_at=timezone.now())
    )


def unread_count_by_conversation(user) -> Dict[int, int]:
    if user is None or getattr(user, "is_anonymous", False):
        return {}
    conversations = Conversation.objects.for_user(user)
    counts = (
        Message.objects.filter(
            conversation__in=conversations,
            read_at__isnull=True,
        )
        .exclude(sender=user)
        .values("conversation_id")
        .annotate(total=Count("id"))
    )
    return {row["conversation_id"]: row["total"] for row in counts}


def _maybe_send_new_message_email(message: Message) -> None:
    conversation = message.conversation
    try:
        recipient = conversation.other_participant(message.sender)
    except ValueError:
        return

    if not recipient.email:
        return

    cache_key = f"chat:email:{conversation.pk}:{recipient.pk}"
    if not cache.add(cache_key, str(message.pk), EMAIL_DEBOUNCE_SECONDS):
        return

    preview = Truncator(strip_tags(message.body)).chars(80)
    context = {
        "recipient": recipient,
        "sender": message.sender,
        "conversation": conversation,
        "message": message,
        "preview": preview,
        "conversation_url": reverse("chat:thread_detail", args=[conversation.pk]),
    }

    subject = render_to_string(
        "chat/email_templates/new_message_subject.txt",
        context,
    ).strip()
    text_body = render_to_string("chat/email_templates/new_message_email.txt", context)
    html_body = render_to_string("chat/email_templates/new_message_email.html", context)

    email = EmailMultiAlternatives(
        subject=subject,
        body=text_body,
        from_email=DEFAULT_FROM_EMAIL,
        to=[recipient.email],
    )
    email.attach_alternative(html_body, "text/html")
    email.send(fail_silently=True)
