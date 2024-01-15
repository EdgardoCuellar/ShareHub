from django.shortcuts import render, redirect
from django.views import View
from store.models.customer import Customer as User
from store.models.forgot_password import ForgotPassword
from store.utils.send_email import send_reset_password

class ForgoPasswordView(View):

    html_template = "customer/forgot_password.html"

    def get(self, request):
        return render(request, self.html_template)
        
    def post(self, request):
        email = request.POST.get('email')

        if User.get_customer_by_email(email):
            user = User.get_customer_by_email(email)
            forgot_password = ForgotPassword.create_forgot_password(user.id)

            send_reset_password(request, forgot_password)

            return render(request, self.html_template, {"success": "Vérifiez vos mails pour réinitialiser votre mot de passe."})
        error = "L'email n'existe pas."
        return render(request, self.html_template, {"error": error})