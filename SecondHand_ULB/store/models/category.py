from django.db import models
from django.core.exceptions import ObjectDoesNotExist

class Category(models.Model):
    name= models.CharField(max_length=50)

    @staticmethod
    def get_category_by_id(id):
        try:
            category = Category.objects.get(id=id)
            return category
        except ObjectDoesNotExist:
            return Category.objects.all()[0]

    @staticmethod
    def get_all_categories():
        return Category.objects.all()

    @staticmethod
    def get_category_by_name(name):
        try:
            category = Category.objects.get(name=name)
            return category
        except ObjectDoesNotExist:
            return Category.objects.all()[0]  # Return None if the category with the given name doesn't exist

    def __str__(self):
        return self.name
