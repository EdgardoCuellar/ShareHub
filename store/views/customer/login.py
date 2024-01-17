from django.shortcuts import render , redirect , HttpResponseRedirect
from django.contrib.auth.hashers import  check_password
from store.models.customer import Customer
from django.views import View
from django.contrib.auth import logout as auth_logout


class Login(View):
    return_url = None

    html_template = "customer/login.html"

    def get(self, request):
        Login.return_url = request.GET.get ('return_url')
        return render (request, self.html_template)

    def post(self, request):
        email = request.POST.get ('email')
        password = request.POST.get ('password')
        customer = Customer.get_customer_by_email (email)
        error_message = None

        if customer:
            if customer.is_banned:
                error_message = 'Votre compte est banni ! Veuillez contacter l\'administrateur.'
                return render (request, self.html_template, {'error': error_message})
            flag = check_password (password, customer.password)
            if flag:
                request.session['customer'] = customer.id
                
                if Login.return_url:
                    return HttpResponseRedirect (Login.return_url)
                else:
                    Login.return_url = None
                    return redirect ('index')
            else:
                error_message = 'Mot de passe invalide !'
        else:
            error_message = 'Votre email n\'est pas enregistré !'

        return render (request, self.html_template, {'error': error_message})

def logout(request):
    auth_logout(request)
    return redirect('login')
