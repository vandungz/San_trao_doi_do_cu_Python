import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from listings.models import Category, Listing

User = get_user_model()

@pytest.mark.django_db
def test_list_page_ok(client):
    url = reverse('listings:list')
    resp = client.get(url)
    assert resp.status_code == 200

@pytest.mark.django_db
def test_create_listing_requires_login(client):
    url = reverse('listings:create')
    resp = client.get(url)
    # redirect to login
    assert resp.status_code in (302, 301)
