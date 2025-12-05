from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import ClubForm, ClubMessageForm
from .models import Club

# Create
@login_required
def create_club(request):
    if request.method == 'POST':
        form = ClubForm(request.POST)
        if form.is_valid():
            club = form.save(commit=False)
            club.creator = request.user
            club.save()
            club.members.add(request.user)
            messages.success(request, f'Clube "{club.name}" criado com sucesso!')
            return redirect('list_clubs')
    else:
        form = ClubForm()

    return render(request, 'club/form.html', {'form': form, 'action': 'create'})

# Read
@login_required
def list_clubs(request):
    clubs = Club.objects.all()
    return render(request, 'club/list.html', {'clubs': clubs})

# Update
@login_required
def edit_club(request, club_id):
    club = get_object_or_404(Club, id=club_id)

    if request.user != club.creator:
        messages.error(request, 'Somente o criador pode editar este clube.')
        return redirect('list_clubs')

    if request.method == 'POST':
        form = ClubForm(request.POST, instance=club)
        if form.is_valid():
            form.save()
            messages.success(request, f'Clube "{club.name}" atualizado com sucesso!')
            return redirect('list_clubs')
    else:
        form = ClubForm(instance=club)

    return render(request, 'club/form.html', {'form': form, 'action': 'edit', 'club': club})

# Delete
@login_required
def delete_club(request, club_id):
    club = get_object_or_404(Club, id=club_id)
    if request.user != club.creator:
        messages.error(request, 'Somente o criador pode excluir este clube.')
        return redirect('list_clubs')

    if request.method == 'POST':
        club.delete()
        messages.success(request, f'Clube "{club.name}" excluído com sucesso!')
        return redirect('list_clubs')

    return render(request, 'club/form.html', {'action': 'delete', 'club': club})

# Detail
@login_required
def club_detail(request, club_id):
    club = get_object_or_404(Club, id=club_id)
    members = club.members.all()

    context = {
        'club': club,
        'members': members,
    }
    return render(request, 'club/detail.html', context)

# Join Club
@login_required
def join_club(request, club_id):
    club = get_object_or_404(Club, id=club_id)
    if request.user in club.members.all():
        messages.info(request, 'Você já é membro deste clube.')
    else:
        club.members.add(request.user)
        messages.success(request, f'Você entrou no clube "{club.name}".')
    return redirect('list_clubs')


# Chat / Mensagens do clube
@login_required
def club_chat(request, club_id):
    club = get_object_or_404(Club, id=club_id)

    if request.user not in club.members.all():
        messages.error(request, 'Você precisa ser membro do clube para ver as mensagens.')
        return redirect('club_detail', club_id=club.id)

    if request.method == 'POST':
        form = ClubMessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.club = club
            message.sender = request.user
            message.save()
            return redirect('club_chat', club_id=club.id)
    else:
        form = ClubMessageForm()

    messages_list = club.messages.all()

    context = {
        'club': club,
        'form': form,
        'messages_list': messages_list
    }
    return render(request, 'club/chat.html', context)

#List User Clubs
@login_required
def list_user_clubs(request, user_id):
    target_user = get_object_or_404(User, id=user_id)
    clubs = Club.objects.filter(members=target_user)
    is_owner = request.user == target_user

    context = {
        'clubs': clubs,
        'target_user': target_user,
        'is_owner': is_owner,
        'page_title': f'Clubes de @{target_user.username}'
    }

    return render(request, 'club/list.html', context)


# Leave Club
@login_required
def leave_club(request, club_id):
    club = get_object_or_404(Club, id=club_id)

    if request.user == club.creator:
        messages.error(request,
                       'O criador do clube não pode sair diretamente. Transfira a propriedade ou exclua o clube.')
        return redirect('club_detail', club_id=club.id)  # Retorna para os detalhes

    if request.user in club.members.all():
        club.members.remove(request.user)
        messages.success(request, f'Você saiu do clube "{club.name}".')
        return redirect('list_clubs')
    else:
        messages.info(request, 'Você não é membro deste clube.')
        return redirect('club_detail', club_id=club.id)