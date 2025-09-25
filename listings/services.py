from __future__ import annotations
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser
from .models import Listing

def submit_for_review(listing: Listing, by_user) -> Listing:
    listing.status = Listing.Status.PENDING
    listing.save(update_fields=['status', 'updated_at'])
    return listing

def publish_listing(listing: Listing, staff_user) -> Listing:
    listing.status = Listing.Status.PUBLISHED
    listing.approved_by = staff_user
    listing.approved_at = timezone.now()
    listing.save(update_fields=['status', 'approved_by', 'approved_at', 'updated_at'])
    return listing
