from django.shortcuts import render

# custom 404 view
def custom_404(request, exception):
    return render(request, 'others/404_not_found.html', status=404)

# custom 500 view
def custom_500(request):
    return render(request, 'others/500_error.html', status=500)