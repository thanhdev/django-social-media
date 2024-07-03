from django.shortcuts import render
from django.contrib.auth.decorators import login_required

def home(request):
    if request.user.is_authenticated:
        return render(request, 'home/authenticated_home.html')
    else:
        return render(request, 'home/index.html')