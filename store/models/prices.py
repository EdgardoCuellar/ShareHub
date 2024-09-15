from django.db import models
from store.models.customer import Customer
from store.models.product import Products
from apscheduler.schedulers.background import BackgroundScheduler
import time
from datetime import timedelta, datetime

class Prices(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE, related_name='product')
    seller = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='seller')
    buyer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='buyer')
    price = models.IntegerField(default=0)
    status = models.IntegerField(default=0)  # 0: offer, 1: accepted, 2: sold, -1: removed
    timestamp = models.IntegerField(default=time.time())
    cooldown_end_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return str(self.price / 100) + '€'

    def start_cooldown(self):
        offers_count = Prices.get_number_of_offers(self.product.id)
        base_time = timedelta(hours=48)  # Base cooldown period of 48 hours
        
        if offers_count > 1:
            # Adjust cooldown period based on the number of offers
            adjusted_time = base_time / offers_count
            self.cooldown_end_time = datetime.now() + adjusted_time
        else:
            self.cooldown_end_time = datetime.now() + base_time

        self.save()
        schedule_offer_acceptance(self)
    
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

    @staticmethod
    def get_number_of_offers(product_id):
        return Prices.get_prices_by_product_id(product_id).count()

# Scheduler for automatic acceptance
def schedule_offer_acceptance(offer):
    scheduler = BackgroundScheduler()

    def accept_offer():
        Prices.accept_offer_by_id(offer.id)
    
    # Schedule the job to run at cooldown_end_time
    scheduler.add_job(accept_offer, 'date', run_date=offer.cooldown_end_time)
    scheduler.start()