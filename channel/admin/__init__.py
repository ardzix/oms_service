from django.contrib import admin
from ..models import Brand, Channel, Event, Product

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ("name", "is_active", "hash")
    list_filter = ("is_active",)
    search_fields = ("name", "description")
    ordering = ("name",)
    readonly_fields = ("hash",)

@admin.register(Channel)
class ChannelAdmin(admin.ModelAdmin):
    list_display = ("name", "brand", "hash")
    list_filter = ("brand",)
    search_fields = ("name", "description", "brand__name")
    ordering = ("name",)
    readonly_fields = ("hash",)

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("name", "channel", "brand", "start_date", "end_date", "hash")
    list_filter = ("brand", "channel", "start_date", "end_date")
    search_fields = ("name", "description", "brand__name", "channel__name")
    ordering = ("-start_date",)
    readonly_fields = ("hash",)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "brand", "channel", "event", "price", "available", "is_valid", "hash")
    list_filter = ("brand", "channel", "event", "available", "is_valid")
    search_fields = ("name", "product_hash", "variant_hash", "brand__name", "channel__name", "event__name")
    ordering = ("name", "price")
    readonly_fields = ("hash",)
    list_editable = ("available", "is_valid", "price")
    autocomplete_fields = ("brand", "channel", "event", "parent")

    fieldsets = (
        ("Basic Info", {"fields": ("name", "description", "brand", "channel", "event", "parent")}),
        ("Identifiers", {"fields": ("hash", "product_hash", "variant_hash")} ),
        ("Status & Pricing", {"fields": ("available", "is_valid", "price")}),
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related("brand", "channel", "event", "parent")
