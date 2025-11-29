from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .forms import SignupForm, PersonForm, AvatarForm, UserDeleteForm
from .models import Person
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = SignupForm()
    return render(request, 'registration/signup.html', {'form': form})

@login_required
def list_(request):
    users = User.objects.all()

    return render(request, 'account/index.html', {'users' : users})

@login_required
def detail(request, user_id=None):

    if user_id is None:
        user_obj = request.user
    else:
        user_obj = get_object_or_404(User, pk=user_id)

    try:
        person = user_obj.person
    except Exception:
        person = None

    is_owner = request.user.is_authenticated and (request.user.pk == user_obj.pk)

    return render(request, 'account/detail.html', { 'person': person, 'user_obj': user_obj, 'is_owner': is_owner})

@login_required
def delete(request):
    user = request.user
    
    delete = True

    if request.method == 'POST':
        user.delete()

        return redirect('account_signup')
    else:
        form = UserDeleteForm(instance=user)

    return render(request, 'account/form.html', {'form': form, 'delete' : delete})

@login_required
def edit_profile(request):
    user = request.user
    person = request.user.person

    edit_profile = True

    if request.method == 'POST':
        form = PersonForm(request.POST, instance=person)
        if form.is_valid():
            form.save()
            return HttpResponse("Voce editou mano!")

    else:
        form = PersonForm(instance=person)

    return render(request, 'account/form.html', {'form': form, 'user': user, 'edit_profile': edit_profile})

@login_required
def edit_avatar(request):
    user = request.user
    person = request.user.person

    edit_avatar = True

    if request.method == 'POST':
        form = AvatarForm(request.POST, request.FILES, instance=person)
        if form.is_valid():
            form.save()
            return HttpResponse("Voce editou o avatar mano!")

    else:
        form = AvatarForm(instance=person)

    return render(request, 'account/form.html', {'form': form, 'user': user, 'edit_avatar': edit_avatar})


