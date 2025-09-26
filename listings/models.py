from django.db import models
from django.contrib.auth.models import User
import os
from uuid import uuid4

def listing_image_upload_to(instance, filename):
    ext = filename.split(".")[-1]
    filename = f"{uuid4().hex}.{ext}"
    return os.path.join("listings", str(instance.listing.id), filename)

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

class Listing(models.Model):
    CONDITION_CHOICES = [("new", "Mới"), ("used", "Đã qua sử dụng")]
    STATUS_CHOICES = [("PENDING", "Chờ duyệt"), ("PUBLISHED", "Đã đăng")]

    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    condition = models.CharField(max_length=20, choices=CONDITION_CHOICES)
    price = models.IntegerField() 
    currency = models.CharField(max_length=10, default="VND")
    location = models.CharField(max_length=200, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="PENDING")
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
     from django.urls import reverse
     return reverse("listings:detail", args=[self.pk])

class ListingImage(models.Model):
    listing = models.ForeignKey(Listing, related_name="images", on_delete=models.CASCADE)
    image = models.ImageField(upload_to=listing_image_upload_to)
    alt_text = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"Ảnh của {self.listing.title}"
