from __future__ import annotations

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


class ConversationQuerySet(models.QuerySet):
    def for_user(self, user):
        if user is None or getattr(user, "is_anonymous", False):
            return self.none()
        return self.filter(models.Q(buyer=user) | models.Q(seller=user))


class Conversation(models.Model):
    listing = models.ForeignKey(
        "listings.Listing",
        on_delete=models.CASCADE,
        related_name="conversations",
    )
    buyer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="chat_conversations_as_buyer",
    )
    seller = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="chat_conversations_as_seller",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    objects = ConversationQuerySet.as_manager()

    class Meta:
        ordering = ("-created_at",)
        constraints = [
            models.UniqueConstraint(
                fields=("listing", "buyer", "seller"),
                name="chat_unique_conversation_per_listing_participants",
            ),
            models.CheckConstraint(
                check=~models.Q(buyer=models.F("seller")),
                name="chat_distinct_participants",
            ),
        ]
        indexes = [
            models.Index(fields=("listing", "created_at")),
            models.Index(fields=("buyer", "created_at")),
            models.Index(fields=("seller", "created_at")),
        ]

    def __str__(self) -> str:
        return f"Conversation(id={self.pk}, listing={self.listing_id})"

    def is_participant(self, user) -> bool:
        if user is None or getattr(user, "is_anonymous", False):
            return False
        return user.pk in (self.buyer_id, self.seller_id)

    def other_participant(self, user):
        if user.pk == self.buyer_id:
            return self.seller
        if user.pk == self.seller_id:
            return self.buyer
        raise ValueError("User is not a participant of this conversation.")

    @property
    def last_message(self):
        if hasattr(self, "_last_messages") and self._last_messages:
            return self._last_messages[0]
        return (
            self.messages.select_related("sender")
            .order_by("-created_at")
            .first()
        )


class MessageQuerySet(models.QuerySet):
    def unread_for(self, user):
        if user is None or getattr(user, "is_anonymous", False):
            return self.none()
        return self.filter(read_at__isnull=True).exclude(sender=user)

    def created_after(self, dt):
        if dt is None:
            return self
        return self.filter(created_at__gt=dt)


class Message(models.Model):
    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name="messages",
    )
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="chat_messages",
    )
    body = models.TextField(max_length=2000)
    created_at = models.DateTimeField(auto_now_add=True)
    read_at = models.DateTimeField(null=True, blank=True)

    objects = MessageQuerySet.as_manager()

    class Meta:
        ordering = ("created_at",)
        indexes = [
            models.Index(fields=("conversation", "created_at")),
        ]

    def __str__(self) -> str:
        return f"Message(id={self.pk}, conversation={self.conversation_id})"

    def clean(self):
        super().clean()
        if not self.conversation_id:
            return
        if self.sender_id not in (
            self.conversation.buyer_id,
            self.conversation.seller_id,
        ):
            raise ValidationError(
                {"sender": "Sender must be a participant of the conversation."}
            )

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    def mark_read(self):
        if not self.read_at:
            self.read_at = timezone.now()
            self.save(update_fields=["read_at"])
