from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm


def home(request):
    if request.user.is_authenticated:
        return render(request, 'home/authenticated_home.html')
    else:
        return render(request, 'home/index.html')


def register(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Welcome, {user.username}! Your account has been created successfully.")
            return redirect('home')
        else:
            messages.error(request, "There was an error with your registration. Please check the form and try again.")
    else:
        form = CustomUserCreationForm()
    return render(request, 'home/register.html', {'form': form})
