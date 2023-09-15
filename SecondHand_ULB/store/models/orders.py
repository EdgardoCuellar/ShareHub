from django.db import models
from .product import Products
from .customer import Customer
import datetime


class Order(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    buyer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name='buyer_orders'  # Specify a related name for the buyer
    )
    seller = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name='seller_orders'  # Specify a related name for the seller
    )
    price = models.IntegerField()
    place_description = models.CharField(max_length=200, default='', blank=True)
    date = models.DateField(default=datetime.datetime.today)
    status = models.BooleanField(default=False)

    def placeOrder(self):
        self.save()

    @staticmethod
    def get_orders_by_buyer(buyer_id):
        return Order.objects.filter(buyer_id=buyer_id).order_by('-date')

    @staticmethod
    def get_orders_by_seller(seller_id):
        return Order.objects.filter(seller_id=seller_id).order_by('-date')


