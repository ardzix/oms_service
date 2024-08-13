import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _

class Brand(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    hash = models.UUIDField(default=uuid.uuid4, editable=True, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Brand")
        verbose_name_plural = _("Brands")

class Channel(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    hash = models.UUIDField(default=uuid.uuid4, editable=True, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Channel")
        verbose_name_plural = _("Channels")

class Event(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    hash = models.UUIDField(default=uuid.uuid4, editable=True, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Event")
        verbose_name_plural = _("Events")

class Product(models.Model):
    parent = models.ForeignKey('self', blank=True, null=True, on_delete=models.CASCADE)
    product_hash = models.CharField(max_length=255, blank=True, null=True)
    variant_hash = models.CharField(max_length=255, blank=True, null=True)
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.SET_NULL, null=True, blank=True)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    available = models.BooleanField(default=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_valid = models.BooleanField(default=True)

    def __str__(self):
        name = f"Variant {self.variant_hash}" if self.variant_hash else f"Product {self.product_hash}"
        return f"{name} on channel {self.channel.name} (event: {self.event})"
    
    def get_product_hash(self):
        product_hash = self.product_hash if self.product_hash else self.parent.get_product_hash()
        return product_hash

    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")
