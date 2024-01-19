from django.db import models
from .product import Products
from .customer import Customer
import datetime


class Order(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    buyer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name='buyer_orders',
        default=None
    )
    seller = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name='seller_orders',
        default=None
    )
    price = models.IntegerField(default=0)
    place_description = models.CharField(max_length=200, default='', blank=True)
    date = models.DateField(default=datetime.datetime.today)
    status = models.BooleanField(default=False)
    rated = models.IntegerField(default=0)

    def placeOrder(self):
        self.save()

    @staticmethod
    def get_order_by_id(order_id):
        return Order.objects.get(id=order_id)

    @staticmethod
    def get_orders_by_buyer(buyer_id):
        return Order.objects.filter(buyer_id=buyer_id).order_by('-date')

    @staticmethod
    def get_orders_by_seller(seller_id):
        return Order.objects.filter(seller_id=seller_id).order_by('-date')


