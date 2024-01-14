from django.shortcuts import render, redirect
from store.models.product import Products
from store.models.category import Category, Condition, Place
from django.views import View
from datetime import datetime
from store.models.customer import Customer
from store.models.product_img import ProductImage


class ModifyProduct (View):

    html_template = "products/modify_product.html"

    def get(self, request, product_id):
        if request.session.get('customer') != Products.get_product_by_id(product_id).customer.id or Products.get_product_by_id(product_id).sold:
            return redirect('homepage')

        categories = Category.get_all_categories()
        conditions = Condition.get_all_conditions()
        places = Place.get_all_places()
        product = Products.get_product_by_id(product_id)
        product.price = product.price / 100

        error = request.session.get('error')
        if error:
            del request.session['error']

        return render (request, self.html_template, {
            'product': product,
            'error': error,
            'categories': categories, 
            'conditions': conditions, 
            'places': places})

    def post(self, request, product_id):
        if request.session.get('customer') != Products.get_product_by_id(product_id).customer.id:
            return redirect('homepage')
        
        product = Products.get_product_by_id(product_id)
        if request.method == 'POST':
            name = request.POST.get('name')
            price = request.POST.get('price')
            date = request.POST.get('date')
            faculty = request.POST.get('faculty')
            condition = request.POST.get('condition')
            place = request.POST.get('place')
            description = request.POST.get('description')
            length = int(request.POST.get('length'))

            if name:
                product.name = name
            if price:
                price = Products.transformPrice(request.POST.get('price'))
                product.price = price
            if date:
                product.date = date
            if faculty:
                product.category = Category.get_category_by_name(faculty)
            if condition:
                product.condition = Condition.get_condition_by_name(condition)
            if place:
                product.place = Place.get_place_by_name(place)
            if description:
                product.description = description
            if length > 0:
                ProductImage.remove_images_by_product_id(product_id)

                for file_num in range(0, int(length)):
                    ProductImage.objects.create(
                    product=product,
                    image=request.FILES.get(f'images{file_num}')
                )

            error_message = self.validateProduct(product)
            
            if not error_message:
                product.save()
                return redirect('product', product.id)  # Redirect to the homepage or any other appropriate page after successful upload

        categories = Category.get_all_categories()
        condition = Condition.get_all_conditions()
        places = Place.get_all_places()

        request.session['error'] = error_message
        
        return redirect("modify_product", product.id)


    def validateProduct(self, product_validation):
        error_message = None
        if len (product_validation.name) < 3:
            error_message = 'Le nom doit contenir au moins 3 caractères'
        elif len (product_validation.name) > 80:
            error_message = 'Le nom ne peut pas contenir plus de 80 caractères'
        elif int(product_validation.price) < 100 or int(product_validation.price) > 10000:
            error_message = "Le prix doit se trouver entre 1 et 100 euro" 
        elif int(product_validation.date) < 2000:
            error_message = "L'année d'achat doit etre au minimum 2000" 
        elif int(product_validation.date) > datetime.now().year:
            error_message = "L'année d'achat ne peut pas être dans le futur"
        elif product_validation.description and len(product_validation.description) >= 300:
            error_message = "La description ne peut pas dépasser 300 caractères"
        elif len(product_validation.description) <= 10:
            error_message = "La description doit au moins faire 10 caractères"

        return error_message
