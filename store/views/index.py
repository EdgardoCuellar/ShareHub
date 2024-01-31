from django.shortcuts import render , redirect , HttpResponseRedirect
from store.models.product import Products
from store.models.category import Category, Condition
from django.views import View
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


class IndexView(View):

    html_link = 'index.html'

    def get(self, request):
        categories = Category.get_all_categories()
        conditions = Condition.get_all_conditions()

        # Get all products
        all_products = Products.get_all_products()

        # Apply filters
        products, values = self.filter(request, all_products)

        products = products.order_by('id')

        # Pagination
        page = request.GET.get('page', 1)
        paginator = Paginator(products, 16)  # Show 16 products per page

        try:
            products = paginator.page(page)
        except PageNotAnInteger:
            products = paginator.page(1)
        except EmptyPage:
            products = paginator.page(paginator.num_pages)

        return render(request, self.html_link, {
            'products': products,
            'values': values,
            'categories': categories,
            'conditions': conditions
        })


    def filter(self, request, products):
        search = request.GET.get('search', '')
        year = request.GET.get('year', '')
        category_id = int(request.GET.get('category', 0))
        type_id = int(request.GET.get('type', 0))

        products = Products.get_all_products()

        if search != '':
            products = products.filter(name__icontains=search)

        if year != '':
            products = products.filter(date=year)

        if category_id != 0:
            products = products.filter(category=category_id)

        if type_id != 0:
            products = products.filter(condition=type_id)

        values = {
            'search': search,
            'year': year,
            'category': category_id,
            'type': type_id
        }

        return products, values


def display_404(request):
    return render(request, 'others/404_not_found.html')

def confidentiality(request):
    return render(request, 'others/confidentiality.html')

def about(request):
    return render(request, 'others/about.html')