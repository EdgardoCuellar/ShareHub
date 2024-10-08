from django.db import models
from django.core.exceptions import ObjectDoesNotExist

class Category(models.Model):
    name= models.CharField(max_length=50, default="")

    def __str__(self):
        return self.name

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
    def get_all_categories_except_last():
        return Category.objects.all().exclude(id=Category.objects.all().last().id)

    @staticmethod
    def get_category_by_name(name):
        try:
            category = Category.objects.get(name=name)
            return category
        except ObjectDoesNotExist:
            return Category.objects.all()[0]  # Return None if the category with the given name doesn't exist

    def __str__(self):
        return self.name

class Condition(models.Model) :
    name= models.CharField(max_length=50)

    @staticmethod
    def get_condition_by_id(id):
        try:
            condition = Condition.objects.get(id=id)
            return condition
        except ObjectDoesNotExist:
            return Condition.objects.all()[0]
    
    @staticmethod
    def get_all_conditions():
        return Condition.objects.all()
    
    @staticmethod
    def get_condition_by_name(name):
        try:
            condition = Condition.objects.get(name=name)
            return condition
        except ObjectDoesNotExist:
            return Condition.objects.all()[0]  # Return None if the condition with the given name doesn't exist

    def __str__(self):
        return self.name

class Place(models.Model):
    name= models.CharField(max_length=50)

    @staticmethod
    def get_place_by_id(id):
        try:
            place = Place.objects.get(id=id)
            return place
        except ObjectDoesNotExist:
            return Place.objects.all()[0]
    
    @staticmethod
    def get_all_places():
        return Place.objects.all()
    
    @staticmethod
    def get_place_by_name(name):
        try:
            place = Place.objects.get(name=name)
            return place
        except ObjectDoesNotExist:
            return Place.objects.all()[0]  # Return None if the place with the given name doesn't exist

    def __str__(self):
        return self.name
