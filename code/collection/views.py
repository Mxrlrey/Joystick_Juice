from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import GameList, GameListItem
from .forms import GameListForm, GameListItemForm
from game.models import Game


def list_lists(request):
    """
    Lista listas públicas e, se logado, também as suas próprias.
    """
    public_lists = GameList.objects.filter(is_public=True).order_by('-created_at')
    if request.user.is_authenticated:
        own_lists = GameList.objects.filter(owner=request.user).order_by('-created_at')
        lists = (public_lists | own_lists).distinct()
    else:
        lists = public_lists

    return render(request, 'collection/list.html', {'lists': lists})


def list_detail(request, pk):
    """
    Mostra uma lista e seus itens. Se for privada, apenas o dono vê.
    """
    gamelist = get_object_or_404(GameList, pk=pk)

    if not gamelist.is_public and (not request.user.is_authenticated or gamelist.owner != request.user):
        return redirect('list_list')

    items = gamelist.items.select_related('game').all().order_by('order', '-added_at')

    item_form = None
    if request.user.is_authenticated and gamelist.owner == request.user:
        item_form = GameListItemForm()

    return render(request, 'collection/detail.html', {
        'gamelist': gamelist,
        'items': items,
        'item_form': item_form,
    })


@login_required
def create_list(request):
    """
    Cria uma nova GameList (POST cria, GET mostra form).
    """
    if request.method == 'POST':
        form = GameListForm(request.POST)
        if form.is_valid():
            gamelist = form.save(commit=False)
            gamelist.owner = request.user
            gamelist.save()
            return redirect('list_detail', pk=gamelist.pk)
    else:
        form = GameListForm()

    return render(request, 'collection/form.html', {'form': form, 'gamelist': None})


@login_required
def edit_list(request, pk):
    """
    Edita uma lista (apenas dono).
    """
    gamelist = get_object_or_404(GameList, pk=pk, owner=request.user)

    if request.method == 'POST':
        form = GameListForm(request.POST, instance=gamelist)
        if form.is_valid():
            form.save()
            return redirect('list_detail', pk=pk)
    else:
        form = GameListForm(instance=gamelist)

    return render(request, 'collection/form.html', {'form': form, 'gamelist': gamelist})


@login_required
def delete_list(request, pk):
    """
    Confirma e deleta uma lista (apenas POST deleta).
    """
    gamelist = get_object_or_404(GameList, pk=pk, owner=request.user)

    if request.method == 'POST':
        gamelist.delete()
        return redirect('list_list')

    return render(request, 'collection/form.html', {'gamelist': gamelist})


@login_required
def add_item(request, list_pk):
    """
    Adiciona um item (jogo) à lista (apenas dono).
    """
    gamelist = get_object_or_404(GameList, pk=list_pk, owner=request.user)

    if request.method == 'POST':
        form = GameListItemForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.list = gamelist
            item.save()
    return redirect('list_detail', pk=list_pk)


@login_required
def edit_item(request, list_pk, item_pk):
    """
    Edita um item da lista (nota, ordem, etc.).
    """
    gamelist = get_object_or_404(GameList, pk=list_pk, owner=request.user)
    item = get_object_or_404(GameListItem, pk=item_pk, list=gamelist)

    if request.method == 'POST':
        form = GameListItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('list_detail', pk=list_pk)
    else:
        form = GameListItemForm(instance=item)

    return render(request, 'collection/form.html', {'form': form, 'gamelist': gamelist, 'item': item})


@login_required
def remove_item(request, list_pk, item_pk):
    """
    Pagina de confirmação e remoção do item (apenas POST remove).
    """
    gamelist = get_object_or_404(GameList, pk=list_pk, owner=request.user)
    item = get_object_or_404(GameListItem, pk=item_pk, list=gamelist)

    if request.method == 'POST':
        item.delete()
        return redirect('list_detail', pk=list_pk)

    return render(request, 'collection/form.html', {'gamelist': gamelist, 'item': item})


@login_required
def quick_toggle_favorite(request, game_id):
    """
    Marca/desmarca um jogo na lista 'Favoritos' do usuário.
    Se a lista 'Favoritos' não existir, é criada aqui (is_public=False).
    Operação sem mensagens; apenas redirect para a página do jogo.
    """
    game = get_object_or_404(Game, pk=game_id)
    user = request.user

    fav_list, _created = GameList.objects.get_or_create(
        owner=user,
        name='Favoritos',
        defaults={'is_public': False}
    )

    existing = GameListItem.objects.filter(list=fav_list, game=game).first()
    if existing:
        existing.delete()
    else:
        # cria o item; supondo que GameListItem tem campos: list, game, note(optional), order(optional)
        GameListItem.objects.create(list=fav_list, game=game)

    return redirect('game_detail', pk=game.pk)
