import grpc
import os
import django

# Configure Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'oms.settings')
django.setup()

from channel.grpc import oms_channel_pb2, oms_channel_pb2_grpc
from django.conf import settings

def print_brand(brand):
    print(f"Brand Hash: {brand.hash}")
    print(f"Name: {brand.name}")
    print(f"Description: {brand.description}")
    print(f"Is Active: {brand.is_active}\n")

def print_channel(channel):
    print(f"Channel Hash: {channel.hash}")
    print(f"Name: {channel.name}")
    print(f"Description: {channel.description}")
    print(f"Brand Hash: {channel.brand_hash}\n")

def print_event(event):
    print(f"Event Hash: {event.hash}")
    print(f"Name: {event.name}")
    print(f"Description: {event.description}")
    print(f"Start Date: {event.start_date}")
    print(f"End Date: {event.end_date}")
    print(f"Channel Hash: {event.channel_hash}")
    print(f"Brand Hash: {event.brand_hash}\n")

def print_product(product):
    print(f"Product Hash: {product.product_hash}")
    print(f"Channel Hash: {product.channel_hash}")
    print(f"Event Hash: {product.event_hash}")
    print(f"Brand Hash: {product.brand_hash}")
    print(f"Available: {product.available}")
    print(f"Price: {product.price}")
    print(f"Is Valid: {product.is_valid}")
    print(f"Hash: {product.hash}\n")

def print_product_variant(variant):
    print(f"Parent Hash: {variant.parent_hash}")
    print(f"Variant Hash: {variant.variant_hash}")
    print(f"Channel Hash: {variant.channel_hash}")
    print(f"Event Hash: {variant.event_hash}")
    print(f"Brand Hash: {variant.brand_hash}")
    print(f"Available: {variant.available}")
    print(f"Price: {variant.price}")
    print(f"Is Valid: {variant.is_valid}")
    print(f"Hash: {variant.hash}\n")

def run():
    with grpc.insecure_channel(f'{settings.OMS_CHANNEL_SERVICE_HOST}:{settings.OMS_CHANNEL_SERVICE_PORT}') as channel:
        stub = oms_channel_pb2_grpc.ChannelServiceStub(channel)

        # List all brands
        print("Listing Brands:")
        brands_response = stub.ListBrands(oms_channel_pb2.Empty())
        for brand in brands_response.brands:
            print_brand(brand)

        # List all channels
        print("Listing Channels:")
        channels_response = stub.ListChannels(oms_channel_pb2.Empty())
        for channel in channels_response.channels:
            print_channel(channel)

        # List all events
        print("Listing Events:")
        events_response = stub.ListEvents(oms_channel_pb2.Empty())
        for event in events_response.events:
            print_event(event)

        # Create a product
        create_product_request = oms_channel_pb2.CreateProductRequest(
            product_hash="e5712557-2a37-481e-bf69-679c708a7398",
            channel_hash="fbb7d89c-be1a-47ac-bf2d-7ecce29295ab",
            event_hash=None,  # Optional
            brand_hash="3e98fa28-0daf-488f-abb5-a280449a6f65",
            available=True,
            price=199.99,
            is_valid=True
        )
        product_response = stub.CreateProduct(create_product_request)
        print("Created Product:")
        print_product(product_response)

        # Get the created product
        get_product_request = oms_channel_pb2.GetProductRequest(hash=product_response.hash)
        product_response = stub.GetProduct(get_product_request)
        print("Retrieved Product:")
        print_product(product_response)

        # Update the product
        update_product_request = oms_channel_pb2.UpdateProductRequest(
            product_hash="e5712557-2a37-481e-bf69-679c708a7398",
            channel_hash="fbb7d89c-be1a-47ac-bf2d-7ecce29295ab",
            event_hash=None,  # Optional
            brand_hash="3e98fa28-0daf-488f-abb5-a280449a6f65",
            available=False,  # Updating availability
            price=149.99,  # Updating price
            is_valid=True,
            hash=product_response.hash
        )
        updated_product_response = stub.UpdateProduct(update_product_request)
        print("Updated Product:")
        print_product(updated_product_response)

        # List products by channel and event (if provided)
        list_products_request = oms_channel_pb2.ListProductsRequest(brand_hash="3e98fa28-0daf-488f-abb5-a280449a6f65", channel_hash="fbb7d89c-be1a-47ac-bf2d-7ecce29295ab")
        products_response = stub.ListProducts(list_products_request)
        print("Listing Products:")
        for product in products_response.products:
            print_product(product)

        # Create a product variant
        create_variant_request = oms_channel_pb2.CreateProductVariantRequest(
            parent_hash=product_response.hash,
            variant_hash="d8d9cce9-fbf4-42e3-9743-05407fca5e0e",
            channel_hash="fbb7d89c-be1a-47ac-bf2d-7ecce29295ab",
            event_hash=None,  # Optional
            brand_hash="3e98fa28-0daf-488f-abb5-a280449a6f65",
            available=True,
            price=179.99,
            is_valid=True
        )
        variant_response = stub.CreateProductVariant(create_variant_request)
        print("Created Product Variant:")
        print_product_variant(variant_response)

        # Get the created product variant
        get_variant_request = oms_channel_pb2.GetProductVariantRequest(hash=variant_response.hash)
        variant_response = stub.GetProductVariant(get_variant_request)
        print("Retrieved Product Variant:")
        print_product_variant(variant_response)

        # Update the product variant
        update_variant_request = oms_channel_pb2.UpdateProductVariantRequest(
            parent_hash=product_response.hash,
            variant_hash="d8d9cce9-fbf4-42e3-9743-05407fca5e0e",
            channel_hash="fbb7d89c-be1a-47ac-bf2d-7ecce29295ab",
            event_hash=None,  # Optional
            brand_hash="3e98fa28-0daf-488f-abb5-a280449a6f65",
            available=False,  # Updating availability
            price=129.99,  # Updating price
            is_valid=True,
            hash=variant_response.hash
        )
        updated_variant_response = stub.UpdateProductVariant(update_variant_request)
        print("Updated Product Variant:")
        print_product_variant(updated_variant_response)

        # List product variants by parent hash
        list_variants_request = oms_channel_pb2.ListProductVariantsRequest(parent_hash=product_response.hash)
        variants_response = stub.ListProductVariants(list_variants_request)
        print("Listing Product Variants:")
        for variant in variants_response.variants:
            print_product_variant(variant)

        # Delete the product variant
        delete_variant_request = oms_channel_pb2.DeleteProductVariantRequest(hash=variant_response.hash)
        stub.DeleteProductVariant(delete_variant_request)
        print(f"Deleted Product Variant with hash: {variant_response.hash}")

        # Delete the product
        delete_product_request = oms_channel_pb2.DeleteProductRequest(hash=product_response.hash)
        stub.DeleteProduct(delete_product_request)
        print(f"Deleted Product with hash: {product_response.hash}")

if __name__ == '__main__':
    run()
