from django.db import models
from .customer import Customer
import hashlib
import datetime

class ForgotPassword(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    token = models.CharField(max_length=256, default=None, null=True, blank=True)
    
    @staticmethod
    def create_forgot_password(user_id):
        forgot_password = ForgotPassword.get_forgot_password_by_user(user_id)
        if forgot_password:
            forgot_password.delete()
        forgot_password = ForgotPassword(customer_id=user_id, token=ForgotPassword.create_token(user_id))
        forgot_password.save()
        return forgot_password

    @staticmethod
    def get_all_forgot_passwords():
        return ForgotPassword.objects.all()
    
    @staticmethod
    def get_forgot_password_by_id(id):
        try:
            return ForgotPassword.objects.get(id=id)
        except:
            return False
        
    @staticmethod
    def get_forgot_password_by_user(user_id):
        try:
            return ForgotPassword.objects.filter(customer=user_id)
        except:
            return False
        
    @staticmethod
    def get_forgot_password_by_token(token):
        try:
            return ForgotPassword.objects.get(token=token)
        except:
            return False
        
    @staticmethod
    def create_token(user_id):
        token = hashlib.sha256((str(user_id) + str(datetime.time) + str(datetime.date)).encode()).hexdigest()
        return token
