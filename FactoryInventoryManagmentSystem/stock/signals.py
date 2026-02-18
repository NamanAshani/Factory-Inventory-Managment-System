# import Django signal which runs after model is saved
from django.db.models.signals import post_save

# decorator to register signal receiver
from django.dispatch import receiver

# import Product and Stock models
from .models import Product, Stock


# listen to post_save event of Product model
@receiver(post_save, sender=Product)
def create_stock_when_product_created(sender, instance, created, **kwargs):
    
    # created=True only when new Product is added (not updated)
    if created:

        # create Stock object automatically
        Stock.objects.create(

            # link this stock to the newly created product
            product=instance,

            # quantities automatically 0 (defaults already exist)
            pre_quantity=0,
            std_quantity=0,
            com_quantity=0,
            eco_quantity=0
        )
