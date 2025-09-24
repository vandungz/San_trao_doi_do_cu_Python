from django.contrib import admin

from .models import Conversation, Message


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ("id", "listing", "buyer", "seller", "created_at")
    search_fields = (
        "listing__title",
        "buyer__username",
        "seller__username",
    )
    list_filter = ("created_at",)
    readonly_fields = ("created_at",)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("id", "conversation", "sender", "created_at", "read_at")
    search_fields = ("body", "sender__username")
    list_filter = ("created_at", "read_at")
    readonly_fields = ("conversation", "sender", "body", "created_at", "read_at")

