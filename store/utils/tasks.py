# tasks.py
from celery import shared_task
from django.utils import timezone
from store.models.product import Products

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
        

