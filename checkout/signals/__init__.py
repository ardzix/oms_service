from django.db.models.signals import post_save
from django.dispatch import receiver
from ..models import Checkout, Invoice
from django.utils.timezone import now

@receiver(post_save, sender=Checkout)
def create_invoice(sender, instance, created, **kwargs):
    if created:
        # Get the current date
        current_date = now()

        # Get the first 4 characters of the brand's hash from the associated cart's brand
        brand_hash_prefix = str(instance.cart.brand.hash)[:4]

        # Generate the incremental number for this month
        year_month = current_date.strftime("%Y%m")
        invoice_count = Invoice.objects.filter(
            created_at__year=current_date.year,
            created_at__month=current_date.month
        ).count() + 1

        # Create the invoice number
        invoice_number = f"INV{year_month}{brand_hash_prefix.upper()}{invoice_count:04d}"

        # Create the invoice
        Invoice.objects.create(
            checkout=instance,
            invoice_number=invoice_number
        )
