from django.db import models
from .product import Products

class ProductImage(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/')

    def __str__(self):
        return self.id

    def register(self):
        self.save()

    def remove(self):
        self.delete()

    @staticmethod
    def get_all_images():
        return ProductImage.objects.all()

    @staticmethod
    def get_image_by_id(id):
        try:
            return ProductImage.objects.get(id=id)
        except:
            return False

    @staticmethod
    def get_images_by_product_id(product_id):
        return ProductImage.objects.filter(product_id=product_id)