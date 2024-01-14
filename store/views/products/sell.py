from django.shortcuts import render, redirect
from store.models.product import Products
from store.models.product_img import ProductImage
from store.models.customer import Customer
from store.models.category import Category, Condition, Place
from django.views import View
from datetime import datetime


class Sell (View):

    html_link = 'products/sell.html'

    def get(self, request):
        categories = Category.get_all_categories()
        conditions = Condition.get_all_conditions()
        places = Place.get_all_places()
        return render (request, self.html_link, {'categories': categories, 'conditions': conditions, 'places': places})

    def post(self, request):
        price = Products.transformPrice(request.POST.get('price'))
        customer_id = request.session.get('customer')
        customer = Customer.get_customer_by_id(customer_id)
        product = Products(name=request.POST.get('name'),
                                price=price,
                                date=request.POST.get('date'),
                                category=Category.get_category_by_name(request.POST.get('category')),
                                condition=Condition.get_condition_by_name(request.POST.get('condition')),
                                place=Place.get_place_by_name(request.POST.get('place')),
                                description=request.POST.get('description'),
                                customer=customer)

        error_message = self.validateProduct(product)
        
        if not error_message:
            product.register()

            length = request.POST.get('length')
            for file_num in range(0, int(length)):
                ProductImage.objects.create(
                    product=product,
                    image=request.FILES.get(f'images{file_num}')
                )

            return redirect('index')  # Redirect to the homepage or any other appropriate page after successful upload

        categories = Category.get_all_categories()
        conditions = Condition.get_all_conditions()
        places = Place.get_all_places()
        return render(request, self.html_link, {'categories': categories, 'conditions': conditions, 'places':places, 'error': error_message})

    def validateProduct(self, product_validation):
        error_message = None
        if (not product_validation.name):
            error_message = "Vous devez entrer un nom !"
        elif len (product_validation.name) < 3:
            error_message = 'Le nom doit contenir au moins 3 caractères'
        elif len (product_validation.name) > 80:
            error_message = 'Le nom ne peut pas contenir plus de 80 caractères'
        elif int(product_validation.price) < 100 or int(product_validation.price) > 10000:
            error_message = "Le prix doit se trouver entre 1 et 100 €" 
        elif int(product_validation.date) < 2000:
            error_message = "L'année d'achat doit etre au minimum 2000" 
        elif int(product_validation.date) > datetime.now().year:
            error_message = "L'année d'achat ne peut pas être dans le futur"
        elif product_validation.description and len(product_validation.description) >= 300:
            error_message = "La description ne peut pas dépasser 300 caractères"
        elif len(product_validation.description) <= 10:
            error_message = "La description doit au moins faire 10 caractères"

        return error_message