from django.shortcuts import render, redirect
from store.models.product import Products
from store.models.category import Category
from django.views import View


class Sell (View):
    def get(self, request):
        categories = Category.get_all_categories()
        return render (request, 'sell.html', {'categories': categories})

    def getCategories(request):
        categories = Category.get_all_categories()

    def post(self, request):
        postData = request.POST
        name = postData.get ('name')
        price = postData.get ('price')
        category = postData.get ('category')
        description = postData.get ('description')
        image = postData.get ('image')
        # validation
        value = {
            'name': name,
            'price': price,
            'image': image
        }
        error_message = None

        category = Category.get_category_by_name(category)

        product = Products (name=name,
                             price=price,
                             category=category,
                             description=description,
                             image=image)
        error_message = self.validateProduct (product)
        if not error_message:
            print(name,price)
            # product.register ()
            return redirect ('homepage')
        else:
            data = {
                'error': error_message,
                'values': value
            }
            return render (request, 'sell.html', data)

    def validateProduct(self, product_validation):
        error_message = None
        if (not product_validation.name):
            error_message = "Vous devez entrer un nom !"
        elif len (product_validation.name) < 5:
            error_message = 'Le nom doit contenir au moins 5 caractères'
        elif not product_validation.price.isdigit():
            error_message = "Le prix doit être un nombre valide"
        elif int(product_validation.price) < 1 or int(product_validation.price) > 100:
            error_message = "Le prix doit se trouver entre 1 et 100 euro" 
        # elif len (product_validation.image) < 3:
        #     error_message = 'Last Name must be 3 char long or more'

        return error_message