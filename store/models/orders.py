from django.db import models
from .product import Products
from .customer import Customer
import datetime

class Order(models.Model):
    # Store details about an order (transaction)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    buyer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='buyer_orders', default=None)
    seller = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='seller_orders', default=None)
    price = models.IntegerField(default=0)  # Price of the order
    place_description = models.CharField(max_length=200, default='', blank=True)  # Place where the item will be exchanged
    date = models.DateField(default=datetime.datetime.today)  # Date when the order was placed
    status = models.BooleanField(default=False)  # Order status (completed or not)
    rated = models.IntegerField(default=0)  # Whether the order has been rated

    def placeOrder(self):
        # Save the order
        self.save()

    @staticmethod
    def get_order_by_id(order_id):
        # Retrieve an order by id
        return Order.objects.get(id=order_id)

    @staticmethod
    def get_orders_by_buyer(buyer_id):
        # Get all orders placed by a buyer
        return Order.objects.filter(buyer_id=buyer_id).order_by('-date')

    @staticmethod
    def get_orders_by_seller(seller_id):
        # Get all orders associated with a seller
        return Order.objects.filter(seller_id=seller_id).order_by('-date')
