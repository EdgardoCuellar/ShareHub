from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.views import View

from django.contrib.auth.hashers import make_password
from store.models.customer import Customer

import random
import string

class ForgoPasswordView(View):

    def get(self, request):
        return render(request, "forgot_password.html")

    def post(self, request):
        email = request.POST.get('email')
        try:
            user = Customer.get_customer_by_email(email)
        except User.DoesNotExist:
            user = None

        if user:
            # Generate a password reset token and send it via email
            key = self.generate_key(user.id)
            
            # Send an email to the user with the reset link
            subject = "Mot de passe oublié - ShareHub"
            message = f"Utilisez cette clé pour vous connecter à votre compte: {key}"
            from_email = "sharehub.ulb@gmail.com"
            recipient_list = [email]

            send_mail(subject, message, from_email, recipient_list)
        
            user.password = make_password(key) 
            user.save()

            return redirect('login') 
        return render(request, "forgot_password.html", {'error': 'L\'adresse email n\'est relié à aucun compte!'})

    def generate_key(self, user):
        random.seed(hash(user))

        # Define the length of the random key
        key_length = 16

        # Generate a random key of 16 characters
        random_key = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(key_length))

        print(random_key)
        return random_key