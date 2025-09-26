from __future__ import annotations
from .models import Listing

def submit_for_review(listing: Listing, by_user) -> Listing:
    listing.status = "PENDING"
    listing.save(update_fields=["status"])
    return listing

def publish_listing(listing: Listing, staff_user) -> Listing:
    listing.status = "PUBLISHED"
    listing.save(update_fields=["status"])
    return listing
