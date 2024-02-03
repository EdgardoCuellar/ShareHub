from django.shortcuts import render , redirect

from django.views import  View

class EdoView(View):

    html_link = 'others/edo.html'

    def get(self , request):
        
        return render(request , self.html_link, {} )