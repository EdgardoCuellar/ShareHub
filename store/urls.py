from django.contrib import admin
from django.urls import path

from .views.homepage import Homepage
from .views.index import IndexView, display_404, confidentiality, price

from .views.customer.signup import Signup
from .views.customer.login import Login , logout
from .views.customer.message import MessagesView
from .views.customer.profile import Profile
from .views.customer.dashboard import DashboardView
from .views.customer.forgot_password import ForgoPasswordView
from .views.customer.reset_password import ResetPasswordView

from .views.products.product import Product, remove
from .views.products.modify_product import ModifyProduct
from .views.products.my_products import MyProductsView
from .views.products.sell import Sell
from .views.products.user_products import UserProductsView
from .views.products.overview import Overview

from .views.proposition import PropositionView
from .views.offers import Offers
from .views.orders import OrderView
from .views.sales import Sales

from .middlewares.auth import  auth_middleware

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', Homepage.as_view(), name='homepage'),
    path('index', IndexView.as_view() , name='index'),

    path('signup', Signup.as_view(), name='signup'),
    path('login', Login.as_view(), name='login'),
    path('logout', logout , name='logout'),
    path('forgot_password/', ForgoPasswordView.as_view(), name='forgot_password'),
    path('reset_password/<str:token>', ResetPasswordView.as_view(), name='reset_password'),

    path('proposition', auth_middleware(PropositionView.as_view()) , name='proposition'),
    path('offers', auth_middleware(Offers.as_view()) , name='offers'),
    path('sell', Sell.as_view(), name='sell'),
    path('orders', auth_middleware(OrderView.as_view()), name='orders'),
    path('sales', auth_middleware(Sales.as_view()), name='sales'),
    path('overview/<int:product_id>/<int:offer_id>', Overview.as_view(), name='overview'),

    path('profile/<int:user_id>', Profile.as_view(), name='profile'),
    path('profile', DashboardView.as_view(), name='profile'),
    path('dashboard', DashboardView.as_view(), name='dashboard'),
    path('dashboard/<str:page>', DashboardView.as_view(), name='dashboard'),
    path('message', MessagesView.as_view(), name='messages'),
    path('message/<int:receiver_id>', MessagesView.as_view(), name='messages'),

    path('product/<int:product_id>', Product.as_view(), name='product'),
    path('product/remove/<int:product_id>', remove, name='product_remove'),
    path('my_products', auth_middleware(MyProductsView.as_view()), name='my_products'),
    path('modify_product/<int:product_id>', ModifyProduct.as_view(), name='modify_product'),
    path('user_products/<int:customer_id>', UserProductsView.as_view(), name='user_products'),

    path('display_404', display_404, name='display_404'), # just a test
    path('confidentiality', confidentiality, name='confidentiality'),
    path('price', price, name='price'),
]