from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .forms import SignupForm, PersonForm, AvatarForm
from .models import Person


def index(request):
    return HttpResponse("Voce logou mano!")

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse("Criou em")
    else:
        form = SignupForm()
    return render(request, 'user/signup.html', {'form': form})

def edit_profile(request):
    person = request.user.person
    user = request.user
    if request.method == 'POST':
        form = PersonForm(request.POST, instance=person)
        if form.is_valid():
            form.save()
            return HttpResponse("Voce editou mano!")

    else:
        form = PersonForm(instance=person)

    return render(request, 'user/edit_profile.html', {'form': form, 'user': user})

def edit_avatar(request):
    person = request.user.person
    user = request.user
    if request.method == 'POST':
        form = AvatarForm(request.POST, request.FILES, instance=person)
        if form.is_valid():
            form.save()
            return HttpResponse("Voce editou o avatar mano!")

    else:
        form = AvatarForm(instance=person)

    return render(request, 'user/edit_avatar.html', {'form': form, 'user': user})