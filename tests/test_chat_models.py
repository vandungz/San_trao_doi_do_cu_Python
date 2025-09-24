import pytest
from django.contrib.auth import get_user_model
from django.core import mail
from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import override_settings

from chat.models import Conversation, Message
from chat.services import (
    RateLimitError,
    create_message,
    mark_read,
    unread_count_by_conversation,
)
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


def _build_listing(owner, title="Ban ghe"):
    return Listing.objects.create(owner=owner, title=title, description="Mo ta")


def test_conversation_unique_constraint(user_factory):
    seller = user_factory(username="seller")
    buyer = user_factory(username="buyer")
    listing = _build_listing(seller)

    Conversation.objects.create(listing=listing, buyer=buyer, seller=seller)

    with pytest.raises(IntegrityError):
        Conversation.objects.create(listing=listing, buyer=buyer, seller=seller)


def test_message_sender_must_be_participant(user_factory):
    seller = user_factory(username="seller")
    buyer = user_factory(username="buyer")
    outsider = user_factory(username="outsider")
    listing = _build_listing(seller)
    conversation = Conversation.objects.create(
        listing=listing,
        buyer=buyer,
        seller=seller,
    )

    with pytest.raises(ValidationError):
        Message.objects.create(
            conversation=conversation,
            sender=outsider,
            body="Xin chao",
        )


@override_settings(EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend")
def test_create_message_only_allows_participants_and_sends_email(user_factory):
    seller = user_factory(username="seller", email="seller@example.com")
    buyer = user_factory(username="buyer", email="buyer@example.com")
    outsider = user_factory(username="outsider")
    listing = _build_listing(seller)
    conversation = Conversation.objects.create(
        listing=listing,
        buyer=buyer,
        seller=seller,
    )

    message = create_message(conversation, buyer, "Xin chao")
    assert message.sender == buyer
    assert message.body == "Xin chao"
    assert mail.outbox
    assert seller.email in mail.outbox[0].to

    with pytest.raises(PermissionError):
        create_message(conversation, outsider, "Khong hop le")


@override_settings(EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend")
def test_create_message_rate_limit(user_factory):
    seller = user_factory(username="seller", email="seller@example.com")
    buyer = user_factory(username="buyer", email="buyer@example.com")
    listing = _build_listing(seller)
    conversation = Conversation.objects.create(
        listing=listing,
        buyer=buyer,
        seller=seller,
    )

    create_message(conversation, buyer, "Lan mot")
    with pytest.raises(RateLimitError):
        create_message(conversation, buyer, "Lan hai")


def test_unread_count_and_mark_read(user_factory):
    seller = user_factory(username="seller")
    buyer = user_factory(username="buyer")
    listing = _build_listing(seller)
    conversation = Conversation.objects.create(
        listing=listing,
        buyer=buyer,
        seller=seller,
    )

    Message.objects.create(conversation=conversation, sender=seller, body="Tin 1")
    Message.objects.create(conversation=conversation, sender=seller, body="Tin 2")
    Message.objects.create(conversation=conversation, sender=buyer, body="Da nhan")

    buyer_unread = unread_count_by_conversation(buyer)
    seller_unread = unread_count_by_conversation(seller)

    assert buyer_unread.get(conversation.pk) == 2
    assert seller_unread.get(conversation.pk) == 1

    updated = mark_read(conversation, buyer)
    assert updated == 2
    assert unread_count_by_conversation(buyer).get(conversation.pk, 0) == 0

