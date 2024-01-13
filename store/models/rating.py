from django.db import models
from django.db.models.fields.related import ForeignKey
from .customer import Customer


class Rating(models.Model):
    user_id = ForeignKey(Customer, on_delete=models.CASCADE, default=None, related_name='user_id')
    user_rated_id = ForeignKey(Customer, on_delete=models.CASCADE, default=None, related_name='user_rated_id')
    rating = models.IntegerField(default=0)
    comment = models.CharField(max_length=250, default='', blank=True, null=True)

    @staticmethod
    def get_count_user_sells(user_id):
        return Rating.objects.filter(user_rated_id=user_id).count()

    @staticmethod
    def get_user_rating(user_id):
        if Rating.get_count_user_sells(user_id) == 0:
            return 0
        else:
            return Rating.objects.filter(user_rated_id=user_id).aggregate(models.Avg('rating'))['rating__avg']

    @staticmethod
    def get_user_id_ratings(user_id):
        return Rating.objects.filter(user_id=user_id)

    @staticmethod
    def get_rating(user_id):
        sell_count = Rating.get_count_user_sells(user_id)
        user_rating = Rating.get_user_rating(user_id)
        rating = {
            'sell_count': sell_count,
            'user_rating': user_rating
        }
        return rating
    