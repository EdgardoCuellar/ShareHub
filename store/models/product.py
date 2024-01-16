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

    @staticmethod
    def validate_image(image):
            # Check if the uploaded file is an image
        if not image:
            return False
        ext = image.name.split('.')[-1].lower()
        if ext not in ['jpg', 'jpeg', 'png']:
            return False

        # Check file size (less than 5MB)
        if image.size > 5 * 1024 * 1024:  # 5MB
            return False

        # Check image dimensions (at least 250x300 pixels)
        from PIL import Image
        img = Image.open(image)
        width, height = img.size
        if width < 200 or height < 250:
            return False

        return True

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