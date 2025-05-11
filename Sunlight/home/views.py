from django.shortcuts import render

# Create your views here.
def home(request):
    """
    View function for the home page of the site.
    """
    return render(request, 'home/index.html')
