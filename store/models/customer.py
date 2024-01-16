from django.db import models

class Customer(models.Model):
    first_name = models.CharField(max_length=50, default="")
    last_name = models.CharField (max_length=50, default="")
    description = models.CharField(max_length=288, default="")
    faculty = models.CharField(max_length=50, default="")
    email=models.EmailField(default="", unique=True)
    password = models.CharField(max_length=100, default="")
    register_date = models.DateField(default=None, null=True, blank=True)

    def isExists(self):
        if Customer.objects.filter(email = self.email):
            return True
        return False

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

    @staticmethod
    def validateCustomer(customer, is_update=False):
        error_message = None
        if (not customer.first_name):
            error_message = "Please Enter your First Name !!"
        elif len (customer.first_name) < 3:
            error_message = 'First Name must be 3 char long or more'
        elif not customer.last_name:
            error_message = 'Please Enter your Last Name'
        elif len (customer.last_name) < 3:
            error_message = 'Last Name must be 3 char long or more'
        elif len (customer.password) < 5:
            error_message = 'Password must be 5 char long'
        elif len (customer.email) < 5:
            error_message = 'Email must be 5 char long'
        elif not is_update and customer.isExists ():
            error_message = 'Email Address Already Registered..'

        return error_message