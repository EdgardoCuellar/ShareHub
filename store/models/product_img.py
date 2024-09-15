from django.db import models
from .product import Products
import os

class ProductImage(models.Model):
    # ForeignKey relationship to associate images with products
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/')

    def __str__(self):
        return str(self.id)

    def register(self):
        self.save()

    def remove(self):
        self.delete()

    @staticmethod
    def get_all_images():
        # Get all product images
        return ProductImage.objects.all()

    @staticmethod
    def get_image_by_id(id):
        try:
            return ProductImage.objects.get(id=id)
        except:
            return False

    @staticmethod
    def get_images_by_product_id(product_id):
        # Get all images associated with a specific product
        return ProductImage.objects.filter(product_id=product_id)

    @staticmethod
    def remove_images_by_product_id(product_id):
        # Delete images associated with a product
        old_images = ProductImage.objects.filter(product_id=product_id)
        for image in old_images:
            image.image.delete()  # Delete the image file
        ProductImage.objects.filter(product_id=product_id).delete()  # Delete image entries
