from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Listing, ListingImage
from .services import publish_listing

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ('name',)

class ListingImageInline(admin.TabularInline):
    model = ListingImage
    extra = 0
    readonly_fields = ["preview"]

    def preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="80" />', obj.image.url)
        return "-"
    preview.short_description = "Ảnh"

@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'status', 'category', 'price', 'owner', 'created_at')
    list_filter = ('status', 'category', 'condition', 'created_at')
    search_fields = ('title', 'description', 'owner__username')
    inlines = [ListingImageInline]
    actions = ['publish_selected']

    def publish_selected(self, request, queryset):
        count = 0
        for obj in queryset.filter(status='PENDING'):
            publish_listing(obj, request.user)
            count += 1
        self.message_user(request, f"Đã publish {count} tin.")
    publish_selected.short_description = "Publish các tin đang PENDING"
