from django.db import models

class Customer(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField (max_length=50)
    description = models.CharField(max_length=288)
    faculty = models.CharField(max_length=50)
    contact = models.CharField(max_length=100)
    email=models.EmailField()
    password = models.CharField(max_length=100)

    #to save the data
    def register(self):
        self.save()

    @staticmethod
    def user_exists(id):
        if Customer.objects.filter(id=id):
            return True
        return False

    @staticmethod
    def get_customer_by_email(email):
        try:
            return Customer.objects.get(email= email)
        except:
            return False

    @staticmethod
    def get_customer_by_id(id):
        try:
            return Customer.objects.get(id= id)
        except:
            return False

    def isExists(self):
        if Customer.objects.filter(email = self.email):
            return True

        return False