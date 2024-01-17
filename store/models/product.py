from django.db import models
from .category import Category, Condition, Place
from .customer import Customer
import random

class Products(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, default=None)
    name = models.CharField(max_length=60, default='')
    price= models.IntegerField(default=0)
    category= models.ForeignKey(Category,on_delete=models.CASCADE,default=1 )
    condition= models.ForeignKey(Condition,on_delete=models.CASCADE,default=1 )
    place= models.ForeignKey(Place,on_delete=models.CASCADE,default=1 )
    description= models.CharField(max_length=250, default='', blank=True, null= True)
    date = models.IntegerField(default=2000)
    sold = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def register(self):
        self.save()

    def remove(self):
        self.delete()

    def validate_product(self):
        error_message = None
        if not self.name:
            error_message = "Veillez entrer le nom de l'article"
        elif len(self.name) < 3:
            error_message = "Le nom de l'article doit contenir au moins 3 caractères"
        elif not self.price:
            error_message = "Veillez entrer le prix de l'article"
        elif not self.description:
            error_message = "Veillez entrer la description de l'article"
        elif len(self.description) < 10:
            error_message = "La description de l'article doit contenir au moins 10 caractères"
        elif not self.date:
            error_message = "Veillez entrer l'année de l'article"
        elif len (product_validation.name) > 80:
            error_message = 'Le nom ne peut pas contenir plus de 80 caractères'
        elif int(product_validation.price) < 100 or int(product_validation.price) > 10000:
            error_message = "Le prix doit se trouver entre 1 et 100 €" 
        elif int(product_validation.date) < 1900:
            error_message = "L'année d'achat doit etre possible" 
        elif int(product_validation.date) > datetime.now().year:
            error_message = "L'année d'achat ne peut pas être dans le futur"
        elif product_validation.description and len(product_validation.description) >= 300:
            error_message = "La description ne peut pas dépasser 300 caractères"
        elif len(product_validation.description) <= 10:
            error_message = "La description doit au moins faire 10 caractères"
        return error_message

    @staticmethod
    def product_exists(id):
        if Products.objects.filter(id=id):
            return True
        return False

    @staticmethod
    def get_product_by_id(id):
        try:
            return Products.objects.get(id=id)
        except:
            return False

    @staticmethod
    def get_products_by_id(ids):
        return Products.objects.filter (id__in=ids)

    @staticmethod
    def get_products_by_userid(customer_id, sold=False):
        if sold:
            return Products.objects.filter (customer=customer_id, sold=True)
        else:
            return Products.objects.filter (customer=customer_id, sold=False)
    
    @staticmethod
    def get_all_products():
        # get all products sold = false
        return Products.objects.filter(sold=False)

    @staticmethod
    def get_all_products_by_categoryid(category_id):
        if category_id:
            return Products.objects.filter (category=category_id)
        else:
            return Products.get_all_products();

    @staticmethod
    def transformPrice(price):
            # check if the number convertable to float
        if not price:
            return 0
        if not price.isdigit():
            return 0
        price = price.replace(',', '.')
        price = float(price)
        price = int(price * 100)

        # Here's the logic to convert the price to our price fixation system
        price = price + random.randint(-int(price * 0.2), int(price * 0.2))

        return price

    @staticmethod
    def price_good_format(price):
        if not price:
            return 0
        if not price.isdigit():
            return 0
        price = price.replace(',', '.')
        price = float(price)
        price = int(price * 100)

        return price