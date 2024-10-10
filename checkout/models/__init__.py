import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from services.catalogue.catalogue_client import CatalogueClient
from services.promo.promo_client import PromoClient


class Checkout(models.Model):
    user_hash = models.CharField(max_length=255)
    hash = models.UUIDField(default=uuid.uuid4, editable=True, unique=True)
    cart = models.ForeignKey("cart.Cart", on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    vat = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    final_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def invoice(self):
        return Invoice.objects.filter(checkout=self).first()
    
    @property
    def cart_items(self):
        return self.cart.cart_items.all()

    def save(self, *args, **kwargs):
        masterdata_client = CatalogueClient()
        promo_client = PromoClient()

        subtotal = float(sum(item.price * item.quantity for item in self.cart_items))
        self.total_price = subtotal

        # Apply promos
        for item in self.cart_items:
            if item.modified_price:
                self.discount += (float(item.price) - float(item.modified_price)) * float(item.quantity)

        discounted_subtotal = subtotal - self.discount

        # Calculate VAT and final price
        vat_rate = masterdata_client.get_vat_rate()
        self.vat = discounted_subtotal * vat_rate
        self.final_price = discounted_subtotal + self.vat

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Checkout {self.hash} - Total: {self.final_price}"

    class Meta:
        verbose_name = _("Checkout")
        verbose_name_plural = _("Checkouts")


class Invoice(models.Model):
    PENDING = "pending"
    PAID = "paid"
    STATUS_CHOICES = [(PENDING, _("Pending")), (PAID, _("Paid"))]

    BRI = "BRI"
    BCA = "BCA"
    BNI = "BNI"
    OVO = "OVO"
    DANA = "DANA"
    LINKAJA = "LINKAJA"
    QR = "QR"
    PAYMENT_METHOD_CHOICES = (
        (BRI, "BRI Virtual Account"),
        (BCA, "BCA Virtual Account"),
        (BNI, "BNI Virtual Account"),
        (OVO, "Ovo E-wallet"),
        (DANA, "Dana E-wallet"),
        (LINKAJA, "LinkAja E-wallet"),
        (QR, "QR Payment (QRIS)"),
    )
    checkout = models.OneToOneField(
        Checkout, on_delete=models.CASCADE, related_name="invoice"
    )
    invoice_number = models.CharField(max_length=100)
    status = models.CharField(max_length=50, default=PENDING, choices=STATUS_CHOICES)
    payment_method = models.CharField(
        max_length=50, default=QR, choices=PAYMENT_METHOD_CHOICES
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.invoice_number

    class Meta:
        verbose_name = _("Invoice")
        verbose_name_plural = _("Invoices")
