from django.db import models
from .category import Category, Condition, Place
class Products(models.Model):
    user_id = models.CharField(max_length=50)
    name = models.CharField(max_length=60)
    price= models.IntegerField(default=0)
    category= models.ForeignKey(Category,on_delete=models.CASCADE,default=1 )
    condition= models.ForeignKey(Condition,on_delete=models.CASCADE,default=1 )
    place= models.ForeignKey(Place,on_delete=models.CASCADE,default=1 )
    description= models.CharField(max_length=250, default='', blank=True, null= True)
    image= models.ImageField(upload_to='products/')
    date = models.IntegerField(default=2000)
    sold = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def register(self):
        self.save()

    def remove(self):
        self.delete()

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
        return price