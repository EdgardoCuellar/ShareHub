from django.db import models
from django.db.models.fields.related import ForeignKey
from .customer import Customer

import time

class Rating(models.Model):
    customer = ForeignKey(Customer, on_delete=models.CASCADE, default=None, related_name='customer')
    customer_rated = ForeignKey(Customer, on_delete=models.CASCADE, default=None, related_name='customer_rated')
    rating = models.IntegerField(default=0)
    comment = models.CharField(max_length=250, default='', blank=True, null=True)
    timestamp = models.IntegerField(default=time.time())

    @staticmethod
    def get_count_user_sells(customer):
        return Rating.objects.filter(customer_rated=customer).count()

    @staticmethod
    def create_rating(customer, customer_rated, rating):
        rating = Rating(customer=customer_rated, customer_rated=customer, rating=rating)
        rating.save()

    @staticmethod
    def get_user_rating(customer_rated):
        if Rating.get_count_user_sells(customer_rated) == 0:
            return 0
        else:
            return Rating.objects.filter(customer_rated=customer_rated).aggregate(models.Avg('rating'))['rating__avg']

    @staticmethod
    def get_user_id_ratings(customer):
        return Rating.objects.filter(customer=customer)

    @staticmethod
    def get_rating(user):
        sell_count = Rating.get_count_user_sells(user)
        user_rating = Rating.get_user_rating(user)
        rating = {
            'sell_count': sell_count,
            'user_rating': user_rating
        }
        return rating
    