from django.shortcuts import render , redirect , HttpResponseRedirect
from store.models.product import Products
from store.models.category import Category
from django.views import View


# Create your views here.
class Index(View):

    def post(self , request):
        product = request.POST.get('product')
        remove = request.POST.get('remove')
        cart = request.session.get('cart')

        request.session['cart'] = cart
        print('cart' , request.session['cart'])
        return redirect('homepage')

    def get(self , request):
        # print()
        return HttpResponseRedirect(f'/store{request.get_full_path()[1:]}')


def store(request):
    cart = request.session.get('cart')
    if not cart:
        request.session['cart'] = {}
    products = None
    categories = Category.get_all_categories()
    
    products, categoryName = filter(request)

    data = {}
    data['products'] = products
    data['categories'] = categories
    data['categoryName'] = categoryName

    return render(request, 'index.html', data)

def filter(request):
    products = None
    categories = Category.get_all_categories()

    nameSearch = request.GET.get('recherche')
    categoryID = request.GET.get('category')
    priceMin = request.GET.get('min')
    priceMax = request.GET.get('max')
    year = request.GET.get('year')

    categoryName = "Tout les syllabus"

    if categoryID and categoryID != '0':
        categoryName = Category.get_category_by_id(categoryID).name
        products = Products.get_all_products_by_categoryid(categoryID)
    else:
        products = Products.get_all_products();
    
    if nameSearch:
        products = products.filter(name__icontains=nameSearch)
    if priceMin:
        products = products.filter(price__gte=priceMin)
    if priceMax:
        products = products.filter(price__lte=priceMax)
    if year:
        products = products.filter(date__gte=year)
    
    return products, categoryName




