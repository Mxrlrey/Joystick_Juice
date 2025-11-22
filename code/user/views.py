from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import SignupForm, LoginForm
from django.contrib.auth import login, logout


def index(request):
    return HttpResponse("Voce logou macaco!")

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponse("Criou em")
    else:
        form = SignupForm()
    return render(request, 'user/signup.html', {'form': form})

