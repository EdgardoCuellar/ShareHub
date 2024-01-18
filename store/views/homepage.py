from django.shortcuts import render , redirect

from django.views import  View

class Homepage(View):
    def get(self , request):
        
        return render(request , 'homepage.html' , {'products' : False} )