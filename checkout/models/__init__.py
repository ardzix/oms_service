import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from services.catalogue.catalogue_client import CatalogueClient
from services.promo.promo_client import PromoClient

class Checkout(models.Model):
    user_hash = models.CharField(max_length=255)
    hash = models.UUIDField(default=uuid.uuid4, editable=True, unique=True)
    cart = models.ForeignKey('cart.Cart', on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    vat = models.DecimalField(max_digits=10, decimal_places=2)
    final_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        masterdata_client = CatalogueClient()
        promo_client = PromoClient()

        cart_items = self.cart.cartitem_set.all()
        subtotal = float(sum(item.price * item.quantity for item in cart_items))
        self.total_price = subtotal

        # Apply promos
        for item in cart_items:
            self.discount += float(item.price) - float(item.modified_price)

        discounted_subtotal = subtotal - self.discount

        # Check threshold promos
        threshold_promo_response = promo_client.check_threshold_promo(subtotal)
        if threshold_promo_response.has_threshold_promo:
            self.discount += threshold_promo_response.discount_value

        # Calculate VAT and final price
        vat_rate = masterdata_client.get_vat_rate()
        self.vat = discounted_subtotal * vat_rate
        self.final_price = discounted_subtotal - self.discount + self.vat

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Checkout {self.hash} - Total: {self.final_price}"

    class Meta:
        verbose_name = _("Checkout")
        verbose_name_plural = _("Checkouts")

class Invoice(models.Model):
    PENDING = 'pending'
    PAID = 'paid'
    STATUS_CHOICES=[(PENDING, _('Pending')), (PAID, _('Paid'))]
    checkout = models.OneToOneField(Checkout, on_delete=models.CASCADE)
    invoice_number = models.CharField(max_length=100)
    status = models.CharField(max_length=50, default=PENDING, choices=STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.invoice_number

    def save(self, *args, **kwargs):
        # Send final invoice to payment service
        # from oms.grpc.clients.payment_client import PaymentClient
        # payment_client = PaymentClient()
        # payment_client.send_invoice(self.invoice_number, self.checkout.final_price)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _("Invoice")
        verbose_name_plural = _("Invoices")
