from datetime import timedelta

import pytest
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.test import Client, override_settings
from django.urls import reverse

from chat.models import Conversation, Message
from listings.models import Listing

pytestmark = pytest.mark.django_db


@pytest.fixture(autouse=True)
def clear_cache():
    cache.clear()


@pytest.fixture
def user_factory():
    User = get_user_model()

    def factory(**kwargs):
        index = factory.counter
        factory.counter += 1
        data = {
            "username": kwargs.pop("username", f"user{index}"),
            "email": kwargs.pop("email", f"user{index}@example.com"),
            "password": kwargs.pop("password", "pass1234"),
        }
        data.update(kwargs)
        return User.objects.create_user(**data)

    factory.counter = 1
    return factory


def _make_conversation(user_factory):
    seller = user_factory(username="seller", email="seller@example.com")
    buyer = user_factory(username="buyer", email="buyer@example.com")
    listing = Listing.objects.create(owner=seller, title="Ban ghe", description="Mo ta")
    conversation = Conversation.objects.create(listing=listing, buyer=buyer, seller=seller)
    return conversation, seller, buyer, listing


def test_threads_view_filters_conversations(client, user_factory):
    conversation, seller, buyer, listing = _make_conversation(user_factory)
    Message.objects.create(conversation=conversation, sender=seller, body="Xin chao")

    other_buyer = user_factory(username="other")
    other_listing = Listing.objects.create(owner=seller, title="Khac", description="Khac")
    Conversation.objects.create(listing=other_listing, buyer=other_buyer, seller=seller)

    client.force_login(buyer)
    response = client.get(reverse("chat:threads"))
    assert response.status_code == 200
    content = response.content.decode()
    assert listing.title in content
    assert other_listing.title not in content


def test_thread_detail_view_blocks_non_participant(client, user_factory):
    conversation, seller, buyer, _ = _make_conversation(user_factory)
    stranger = user_factory(username="stranger")

    client.force_login(stranger)
    response = client.get(reverse("chat:thread_detail", args=[conversation.pk]))
    assert response.status_code == 403


@override_settings(EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend")
def test_post_message_creates_message_and_returns_partial(client, user_factory):
    conversation, seller, buyer, _ = _make_conversation(user_factory)
    client.force_login(buyer)

    url = reverse("chat:thread_send", args=[conversation.pk])
    response = client.post(
        url,
        {"body": " <b>Hello</b> "},
        HTTP_HX_REQUEST="true",
    )

    assert response.status_code == 201
    new_message = Message.objects.filter(conversation=conversation).latest("created_at")
    assert new_message.sender == buyer
    assert "&lt;b&gt;Hello&lt;/b&gt;" in new_message.body
    seller_unread = Message.objects.filter(
        conversation=conversation,
        sender=buyer,
        read_at__isnull=True,
    ).count()
    assert seller_unread == 1
    assert "X-Last-Timestamp" in response.headers


def test_poll_messages_view_returns_new_messages(client, user_factory):
    conversation, seller, buyer, _ = _make_conversation(user_factory)
    message = Message.objects.create(conversation=conversation, sender=seller, body="Xin chao")

    client.force_login(buyer)
    earlier = (message.created_at - timedelta(seconds=1)).isoformat()
    response = client.get(
        reverse("chat:thread_poll", args=[conversation.pk]),
        {"after": earlier},
        HTTP_ACCEPT="application/json",
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["messages"][0]["body"] == "Xin chao"
    assert payload["messages"][0]["is_self"] is False


def test_start_conversation_redirects(client, user_factory):
    conversation, seller, buyer, listing = _make_conversation(user_factory)
    conversation.delete()

    client.force_login(buyer)
    response = client.get(
        reverse("chat:start_conversation", args=[listing.pk, seller.pk])
    )

    assert response.status_code == 302
    created = Conversation.objects.get(listing=listing, buyer=buyer, seller=seller)
    assert str(created.pk) in response.headers["Location"]


def test_post_without_csrf_is_forbidden(user_factory):
    conversation, seller, buyer, _ = _make_conversation(user_factory)
    csrf_client = Client(enforce_csrf_checks=True)
    csrf_client.force_login(buyer)

    response = csrf_client.post(
        reverse("chat:thread_send", args=[conversation.pk]),
        {"body": "Hello"},
    )
    assert response.status_code == 403
