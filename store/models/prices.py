from django.db import models
from store.models.customer import Customer
from store.models.product import Products
import time

class Prices(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE, related_name='product')
    seller = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='seller')
    buyer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='buyer')
    price = models.IntegerField(default=0)
    status = models.IntegerField(default=0) # 0: offer, 1: accepted, 2: sold, -1: removed
    timestamp = models.IntegerField(default=time.time())
    timestamp_status = models.IntegerField(default=time.time(), null=True, blank=True) # date when the status changed

    def __str__(self):
        return str(self.price / 100) + '€'
    
    @staticmethod
    def get_prices_by_product_id(product_id):
        return Prices.objects.filter(product=product_id).filter(status=0)
    
    @staticmethod
    def get_prices_by_seller_id(seller_id):
        return Prices.objects.filter(seller=seller_id).filter(status=0)
    
    @staticmethod
    def get_prices_by_buyer_id(buyer_id):
        return Prices.objects.filter(buyer=buyer_id).filter(status=0)
    
    @staticmethod
    def get_price_by_buyer_product(buyer_id, product_id):
        return Prices.get_prices_by_buyer_id(buyer_id).filter(product=product_id).filter(status=0)

    @staticmethod
    def is_already_offer(buyer_id, product_id):
        return Prices.get_price_by_buyer_product(buyer_id, product_id).filter(status=0).exists()

    @staticmethod
    def remove_buyer_product_offer(buyer_id, product_id):
        Prices.get_price_by_buyer_product(buyer_id, product_id).filter(status=0).update(status=-1, timestamp_status=time.time())

    @staticmethod
    def remove_offer_by_id(id):
        Prices.objects.filter(id=id).filter(status=0).update(status=-1, timestamp_status=time.time())
    
    @staticmethod
    def refuse_offer_by_id(id):
        Prices.objects.filter(id=id).filter(status=0).update(status=1, timestamp_status=time.time())

    @staticmethod
    def accept_offer_by_id(id):
        Prices.objects.filter(id=id).filter(status=0).update(status=2, timestamp_status=time.time())
        return Prices.objects.filter(id=id).filter(status=2)[0]

    @staticmethod
    def get_price_by_id(id):
        return Prices.objects.filter(id=id).filter(status=0)[0]

    @staticmethod
    def get_price_by_id_accepted(id):
        try :
            return Prices.objects.filter(id=id).filter(status=2)[0]
        except :
            return False
    
    @staticmethod
    def get_all_prices():
        return Prices.objects.all().filter(status=0)