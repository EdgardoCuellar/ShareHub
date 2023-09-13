from django.db import models
from .customer import Customer


class Rating(models.Model):
    user_id = models.IntegerField()
    user_rated_id = models.IntegerField()
    rating = models.IntegerField(default=0)


    def rateUser(self):
        self.save()

    @staticmethod
    def get_count_user_sells(user_id):
        return Rating.objects.filter(user_rated_id=user_id).count()

    @staticmethod
    def get_user_rating(user_id):
        # get the mean of the user ratings, using my static method get_count_user_sells
        # return the mean
        # if the user has no ratings, return 0
        if Rating.get_count_user_sells(user_id) == 0:
            return 0
        else:
            return Rating.objects.filter(user_id=user_id).aggregate(models.Avg('rating'))['rating__avg']