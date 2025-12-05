from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponseForbidden
from django.contrib import messages

from .models import GameList, GameListItem
from .forms import GameListForm, GameListItemForm
from game.models import Game
from django.views.decorators.http import require_POST
from django.http import JsonResponse
import json

def user_is_owner(obj, user):
    return hasattr(obj, "owner") and obj.owner == user


@login_required
def user_lists(request):
    """
    Renderiza collection/user_list.html e fornece 'user_lists' no contexto.
    """
    user_lists = GameList.objects.filter(owner=request.user).order_by('-created_at')

    context = {
        "user_lists": user_lists,
    }
    return render(request, "collection/user_list.html", context)

def public_lists(request):
    """
    Mostra somente as listas públicas de outros usuários.
    """
    lists = GameList.objects.filter(is_public=True)

    if request.user.is_authenticated:
        lists = lists.exclude(owner=request.user)

    context = {
        "public_others": lists,
    }
    return render(request, "collection/list.html", context)


@login_required
def create_list(request):
    """Create a new GameList (owner = request.user)."""
    if request.method == "POST":
        form = GameListForm(request.POST)
        if form.is_valid():
            new_list = form.save(commit=False)
            new_list.owner = request.user
            new_list.save()
            messages.success(request, "Lista criada com sucesso.")
            return redirect("list_detail", pk=new_list.pk)
    else:
        form = GameListForm()
    return render(request, "collection/form.html", {"form": form})


@login_required
def list_detail(request, pk):
    """Show a list and its items. Only owner or public lists visible."""
    game_list = get_object_or_404(GameList, pk=pk)
    if not game_list.is_public and not user_is_owner(game_list, request.user):
        raise Http404()
    items = game_list.items.select_related("game").all()
    return render(request, "collection/detail.html", {"list": game_list, "items": items})


@login_required
def edit_list(request, pk):
    """Edit a GameList (only owner)."""
    game_list = get_object_or_404(GameList, pk=pk)
    if not user_is_owner(game_list, request.user):
        return HttpResponseForbidden("Você não tem permissão para editar esta lista.")

    if request.method == "POST":
        form = GameListForm(request.POST, instance=game_list)
        if form.is_valid():
            form.save()
            messages.success(request, "Lista atualizada.")
            return redirect("list_detail", pk=game_list.pk)
    else:
        form = GameListForm(instance=game_list)
    return render(request, "collection/form.html", {"form": form, "list": game_list})


@login_required
def delete_list(request, pk):
    """Delete a GameList (only owner). Confirm via POST."""
    game_list = get_object_or_404(GameList, pk=pk)
    if not user_is_owner(game_list, request.user):
        return HttpResponseForbidden("Você não tem permissão para deletar esta lista.")

    if request.method == "POST":
        game_list.delete()
        messages.success(request, "Lista deletada.")
        return redirect("user_lists")
    return render(request, "collection/form.html", {"list": game_list})

@login_required
def add_item(request, list_pk):
    """Add an item to a list. list_pk required in URL."""
    game_list = get_object_or_404(GameList, pk=list_pk)
    if not user_is_owner(game_list, request.user):
        return HttpResponseForbidden("Você não tem permissão para adicionar itens a esta lista.")

    if request.method == "POST":
        form = GameListItemForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.list = game_list
            try:
                item.save()
                messages.success(request, "Item adicionado à lista.")
            except Exception as e:
                messages.error(request, f"Não foi possível adicionar: {e}")
            return redirect("list_detail", pk=list_pk)
    else:
        form = GameListItemForm()
    return render(request, "collection/form.html", {"form": form, "list": game_list})


@login_required
def edit_item(request, list_pk, item_pk):
    """Edit an item in a list (only owner of the list)."""
    game_list = get_object_or_404(GameList, pk=list_pk)
    if not user_is_owner(game_list, request.user):
        return HttpResponseForbidden("Você não tem permissão para editar itens desta lista.")

    item = get_object_or_404(GameListItem, pk=item_pk, list=game_list)

    if request.method == "POST":
        form = GameListItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, "Item atualizado.")
            return redirect("list_detail", pk=list_pk)
    else:
        form = GameListItemForm(instance=item)
    return render(request, "collection/form.html", {"form": form, "list": game_list, "item": item})


@login_required
def remove_item(request, list_pk, item_pk):
    """Remove an item from a list (only owner). Confirm via POST."""
    game_list = get_object_or_404(GameList, pk=list_pk)
    if not user_is_owner(game_list, request.user):
        return HttpResponseForbidden("Você não tem permissão para remover itens desta lista.")

    item = get_object_or_404(GameListItem, pk=item_pk, list=game_list)
    if request.method == "POST":
        item.delete()
        messages.success(request, "Item removido.")
        return redirect("list_detail", pk=list_pk)
    return render(request, "collection/form.html", {"item": item, "list": game_list})


@require_POST
def reorder_list(request, list_pk):
    data = json.loads(request.body)
    order = data.get("order", [])

    for index, item_id in enumerate(order):
        GameListItem.objects.filter(pk=item_id, list_id=list_pk).update(order=index)

    return JsonResponse({"status": "ok"})