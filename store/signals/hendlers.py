from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from store.models import Customer, Cart, Favorite, Product
import logging

logger = logging.getLogger(__name__)
User = get_user_model()


@receiver(post_save, sender=User)
def setup_customer_cart_and_favorite(sender, instance, created, **kwargs):
    if not created:
        return

    try:
        customer, _ = Customer.objects.get_or_create(user=instance)
        logger.info(f"[SIGNAL] Customer created for user {instance.id}")
    except Exception as e:
        logger.error(f"[SIGNAL] Failed to create Customer: {e}")
        return  

    try:
        Cart.objects.get_or_create(user=instance)
        logger.info(f"[SIGNAL] Cart created for user {instance.id}")
    except Exception as e:
        logger.error(f"[SIGNAL] Failed to create Cart: {e}")

    try:
        product = Product.objects.first() 
        if product:
            Favorite.objects.get_or_create(customer=customer, product=product)
            logger.info(f"[SIGNAL] Favorite created for customer {customer.id}")
    except Exception as e:
        logger.warning(f"[SIGNAL] Skipped creating Favorite: {e}")

