from django.shortcuts import render, redirect
from store.models.product import Products
from store.models.category import Category
from django.views import View


class Sell (View):
    def get(self, request):
        categories = Category.get_all_categories()
        return render (request, 'sell.html', {'categories': categories})

    def post(self, request):
        product = Products(name=request.POST.get('name'),
                                price=request.POST.get('price'),
                                category=Category.get_category_by_name(request.POST.get('category')),
                                description=request.POST.get('description'),
                                image=request.FILES.get('image'),
                                user_id=request.session.get('customer'))

        error_message = self.validateProduct(product)
        print(error_message)
        if not error_message:
            product.register()
            return redirect('homepage')  # Redirect to the homepage or any other appropriate page after successful upload

        categories = Category.get_all_categories()
        return render(request, 'sell.html', {'categories': categories, 'error': error_message})




    def validateProduct(self, product_validation):
        error_message = None
        if (not product_validation.name):
            error_message = "Vous devez entrer un nom !"
        elif len (product_validation.name) < 3:
            error_message = 'Le nom doit contenir au moins 3 caractères'
        elif not product_validation.price.isdigit():
            error_message = "Le prix doit être un nombre valide"
        elif int(product_validation.price) < 1 or int(product_validation.price) > 100:
            error_message = "Le prix doit se trouver entre 1 et 100 euro" 
        # elif len (product_validation.image) < 3:
        #     error_message = 'Last Name must be 3 char long or more'

        return error_message