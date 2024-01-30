# tasks.py
from celery import shared_task
from django.utils import timezone
from store.models.product import Products
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

@shared_task
def your_delayed_task(product_id):
    # Get the item and perform your desired actions
    product = Products.objects.get(id=product_id)

    # Check if 24 hours have passed
    if timezone.now() - product.timestamp >= timezone.timedelta(hours=24):
        
        # create a file .txt with the product details 
        file = open("product.txt", "w")
        file.write("Product name: " + product.name + "\n")
        file.write("Product description: " + product.description + "\n")
        file.write("Product price: " + str(product.price) + "\n")
        file.write("Product date: " + str(product.date) + "\n")
        file.close()
        

@receiver(post_save, sender=Products)
def schedule_delayed_task(sender, instance, **kwargs):
    # Schedule the task after 24 hours
    eta = timezone.now() + timezone.timedelta(hours=24)
    your_delayed_task.apply_async(args=[instance.pk], eta=eta)