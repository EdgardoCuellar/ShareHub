from django.shortcuts import render, redirect
from store.models.product import Products
from store.models.category import Category
from django.views import View
from datetime import datetime


class Sell (View):
    def get(self, request):
        categories = Category.get_all_categories()
        return render (request, 'sell.html', {'categories': categories})

    def post(self, request):
        price = self.transformPrice(request.POST.get('price'))
        product = Products(name=request.POST.get('name'),
                                price=request.POST.get('price'),
                                date=request.POST.get('date'),
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

    def transformPrice(self, price):
        # check if the number convertable to float
        if not price:
            return 0
        if not price.isdigit():
            return 0
        price = price.replace(',', '.')
        price = float(price)
        price = int(price * 100)
        return price

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
        elif int(product_validation.date) < 2000:
            error_message = "L'année d'achat doit etre au minimum 2000" 
        elif int(product_validation.date) > datetime.now().year:
            error_message = "L'année d'achat ne peut pas être dans le futur"

        return error_message