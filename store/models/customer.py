from django.db import models

class Customer(models.Model):
    first_name = models.CharField(max_length=50, default="")
    last_name = models.CharField (max_length=50, default="")
    description = models.CharField(max_length=288, default="")
    faculty = models.CharField(max_length=50, default="")
    email=models.EmailField(default="", unique=True)
    password = models.CharField(max_length=100, default="")
    register_date = models.DateField(default=None, null=True, blank=True)
    is_banned = models.BooleanField(default=False)

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
            error_message = "Veillez entrer votre prénom"
        elif len (customer.first_name) < 3:
            error_message = 'Votre prénom doit contenir au moins 3 caractères'
        elif not customer.last_name:
            error_message = 'Veillez entrer votre prénom'
        elif len (customer.last_name) < 3:
            error_message = 'Votre nom doit contenir au moins 3 caractères'
        elif len (customer.password) < 8:
            error_message = 'Votre mot de passe doit contenir au moins 8 caractères'
        elif not any (char.isdigit () for char in customer.password):
            error_message = 'Votre mot de passe doit contenir au moins un chiffre'
        elif not any (char.isalpha () for char in customer.password):
            error_message = 'Votre mot de passe doit contenir au moins une lettre'
        elif not customer.email:
            error_message = 'Veillez entrer votre email'
        elif len (customer.email) < 6:
            error_message = 'Votre email doit contenir au moins 6 caractères'
        # verify if email is valid
        elif not customer.email.__contains__ ('@'):
            error_message = 'Votre email doit contenir un @'
        elif not customer.faculty:
            error_message = 'Veillez entrer votre faculté'
        
        elif not is_update and customer.isExists ():
            error_message = 'Vous avez déjà un compte avec cet email !'

        elif customer.is_banned:
            error_message = 'Votre compte est banni !'

        return error_message