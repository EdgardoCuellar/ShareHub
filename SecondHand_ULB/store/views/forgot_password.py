from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.views import View


class ForgoPasswordView(View):

    def get(self, request):
        return render(request, "forgot_password.html")

    def post(self, request):
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = None

        if user:
            # Generate a password reset token and send it via email
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))

            reset_link = f"http://yourwebsite.com/reset_password/{uid}/{token}/"

            # Send an email to the user with the reset link
            subject = "Password Reset"
            message = f"Click the following link to reset your password: {reset_link}"
            from_email = "your_email@example.com"
            recipient_list = [email]

            send_mail(subject, message, from_email, recipient_list)

            return render(request, "password_reset_email_sent.html")  # Create this template
