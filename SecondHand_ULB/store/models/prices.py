from django.db import models
from store.models.customer import Customer
from store.models.product import Products

class Prices(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE, related_name='product')
    seller = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='seller')
    buyer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='buyer')
    price = models.IntegerField()

    def __str__(self):
        return str(self.price / 100) + '€'
    
    @staticmethod
    def get_prices_by_product_id(product_id):
        return Prices.objects.filter(product=product_id)
    
    @staticmethod
    def get_prices_by_seller_id(seller_id):
        return Prices.objects.filter(seller=seller_id)
    
    @staticmethod
    def get_prices_by_buyer_id(buyer_id):
        return Prices.objects.filter(buyer=buyer_id)
    
    @staticmethod
    def get_price_by_buyer_product(buyer_id, product_id):
        return Prices.get_prices_by_buyer_id(buyer_id).filter(product=product_id)
    
    @staticmethod
    def get_price_by_id(id):
        return Prices.objects.filter(id=id)[0]
    
    @staticmethod
    def get_all_prices():
        return Prices.objects.all()