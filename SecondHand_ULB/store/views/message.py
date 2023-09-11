from django.shortcuts import render, redirect
from store.models.customer import Customer
from django.views import View
from store.middlewares.auth import auth_middleware

class Message(View):


    def get(self , request ):
        
        print("hey")
        messages = "heyyyyyy"
        return render(request , 'message.html'  , {'messages' : messages})
