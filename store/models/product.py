from django.db import models
from .category import Category, Condition, Place
from .customer import Customer
from datetime import datetime
import time
import random

# Constants for accepting offers
MIN_TIME_BEFORE_ACCEPT_OFFER = 1 * 60 * 60 * 24  # 1 day in seconds
MIN_OFFERS_BEFORE_ACCEPT_OFFER = 2  # Minimum number of offers required before accepting one
MIN_TIME_BEFORE_ACCEPT_SINGLE_OFFER = 2 * 60 * 60 * 24  # Time before seller can accept a single offer

class Products(models.Model):
    # ForeignKey relationships for customer, category, condition, and place
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, default=None)
    name = models.CharField(max_length=60, default='')
    price = models.IntegerField(default=0)  # Price is in cents for better precision
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    condition = models.ForeignKey(Condition, on_delete=models.CASCADE, default=1)
    place = models.ForeignKey(Place, on_delete=models.CASCADE, default=1)
    description = models.CharField(max_length=250, default='', blank=True, null=True)
    date = models.IntegerField(default=2000)  # Year of the product
    sold = models.BooleanField(default=False)  # Whether the product is sold
    timestamp = models.IntegerField(default=time.time())  # Unix timestamp
    listed = models.BooleanField(default=True)  # If the product is still listed

    def __str__(self):
        return self.name

    def register(self):
        self.timestamp = time.time()  # Update the timestamp to the current time
        self.save()

    def force_delete(self):
        self.delete()

    def remove(self):
        self.listed = False  # Mark the product as unlisted, don't delete
        self.save()

    def validate_product(self):
        # Basic validation for the product fields
        error_message = None
        if not self.name:
            error_message = "Veillez entrer le nom de l'article"
        elif len(self.name) < 3:
            error_message = "Le nom de l'article doit contenir au moins 3 caractères"
        elif not self.price:
            error_message = "Veillez entrer le prix de l'article"
        elif not self.description:
            error_message = "Veillez entrer la description de l'article"
        elif not self.date:
            error_message = "Veillez entrer l'année de l'article"
        elif len(self.name) > 80:
            error_message = 'Le nom ne peut pas contenir plus de 80 caractères'
        elif int(self.price) < 100 or int(self.price) > 10000:
            error_message = "Le prix doit se trouver entre 1 et 100 €"
        elif int(self.date) < 1900:
            error_message = "L'année d'achat doit etre possible"
        elif int(self.date) > datetime.now().year:
            error_message = "L'année d'achat ne peut pas être dans le futur"
        elif self.description and len(self.description) >= 300:
            error_message = "La description ne peut pas dépasser 300 caractères"
        return error_message

    @staticmethod
    def product_exists(id):
        # Check if a product with the given id exists and is listed
        if Products.objects.filter(id=id, listed=True).exists():
            return True
        return False

    @staticmethod
    def get_product_by_id(id):
        # Retrieve a product by id, if listed
        try:
            return Products.objects.get(id=id, listed=True)
        except:
            return False

    @staticmethod
    def get_products_by_id(ids):
        # Get multiple products by ids
        return Products.objects.filter(id__in=ids)

    @staticmethod
    def get_products_by_userid(customer_id, sold=False):
        # Get products for a specific user, filter by sold status
        if sold:
            return Products.objects.filter(customer=customer_id, sold=True, listed=True)
        else:
            return Products.objects.filter(customer=customer_id, sold=False, listed=True)

    @staticmethod
    def get_all_products():
        # Get all available products that are not sold and listed
        return Products.objects.filter(sold=False, listed=True)

    @staticmethod
    def get_all_products_by_categoryid(category_id):
        # Get products filtered by category
        if category_id:
            return Products.objects.filter(category=category_id, sold=False, listed=True)
        else:
            return Products.get_all_products()

    @staticmethod
    def is_float(string):
        # Check if a string can be converted to a float
        try:
            float(string)
            return True
        except ValueError:
            return False

    @staticmethod
    def price_good_format(price):
        # Clean and format the price as an integer (cents)
        if not price:
            return 0
        price = price.replace(',', '.')
        if not Products.is_float(price):
            return 0
        price = float(price)
        price = int(price * 100)
        return price

    @staticmethod
    def remove_product_by_id(id):
        # Mark the product as unlisted (soft delete)
        Products.objects.filter(id=id).update(listed=False)
