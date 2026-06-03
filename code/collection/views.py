import json

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import Http404, HttpResponseForbidden, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView, View

from collection.forms import GameListForm, GameListItemForm
from collection.models import GameList, GameListItem


def user_is_owner(obj, user):
    return hasattr(obj, 'owner') and obj.owner == user


class ListOwnerRequiredMixin(UserPassesTestMixin):
    permission_denied_message = 'Você não tem permissão para editar esta lista.'

    def test_func(self):
        return user_is_owner(self.get_object(), self.request.user)

    def handle_no_permission(self):
        return HttpResponseForbidden(self.permission_denied_message)


class ItemListOwnerRequiredMixin(UserPassesTestMixin):
    permission_denied_message = 'Você não tem permissão para editar itens desta lista.'

    def dispatch(self, request, *args, **kwargs):
        self.game_list = get_object_or_404(GameList, pk=kwargs['list_pk'])
        return super().dispatch(request, *args, **kwargs)

    def test_func(self):
        return user_is_owner(self.game_list, self.request.user)

    def handle_no_permission(self):
        return HttpResponseForbidden(self.permission_denied_message)


class UserListsView(LoginRequiredMixin, ListView):
    template_name = 'collection/user_list.html'
    context_object_name = 'user_lists'

    def get_queryset(self):
        return GameList.objects.filter(owner=self.request.user).order_by('-created_at')


class PublicListsView(ListView):
    template_name = 'collection/list.html'
    context_object_name = 'public_others'

    def get_queryset(self):
        queryset = GameList.objects.filter(is_public=True)
        if self.request.user.is_authenticated:
            queryset = queryset.exclude(owner=self.request.user)
        return queryset


class GameListCreateView(LoginRequiredMixin, CreateView):
    model = GameList
    form_class = GameListForm
    template_name = 'collection/form.html'

    def form_valid(self, form):
        form.instance.owner = self.request.user
        response = super().form_valid(form)
        messages.success(self.request, 'Lista criada com sucesso.')
        return response

    def get_success_url(self):
        return reverse_lazy('list_detail', kwargs={'pk': self.object.pk})


class GameListDetailView(LoginRequiredMixin, DetailView):
    model = GameList
    pk_url_kwarg = 'pk'
    template_name = 'collection/detail.html'
    context_object_name = 'list'

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if not self.object.is_public and not user_is_owner(self.object, request.user):
            raise Http404()
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['items'] = self.object.items.select_related('game').all()
        return context


class GameListUpdateView(LoginRequiredMixin, ListOwnerRequiredMixin, UpdateView):
    model = GameList
    form_class = GameListForm
    pk_url_kwarg = 'pk'
    template_name = 'collection/form.html'
    context_object_name = 'list'

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Lista atualizada.')
        return response

    def get_success_url(self):
        return reverse_lazy('list_detail', kwargs={'pk': self.object.pk})


class GameListDeleteView(LoginRequiredMixin, ListOwnerRequiredMixin, DetailView):
    model = GameList
    pk_url_kwarg = 'pk'
    template_name = 'collection/form.html'
    context_object_name = 'list'
    permission_denied_message = 'Você não tem permissão para deletar esta lista.'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        messages.success(request, 'Lista deletada.')
        return redirect('user_lists')


class GameListItemCreateView(LoginRequiredMixin, View):
    def dispatch(self, request, *args, **kwargs):
        self.game_list = get_object_or_404(GameList, pk=kwargs['list_pk'])
        if not user_is_owner(self.game_list, request.user):
            return HttpResponseForbidden('Você não tem permissão para adicionar itens a esta lista.')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return render(request, 'collection/form.html', {'form': GameListItemForm(), 'list': self.game_list})

    def post(self, request, *args, **kwargs):
        form = GameListItemForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.list = self.game_list
            try:
                item.save()
                messages.success(request, 'Item adicionado à lista.')
            except Exception as exc:
                messages.error(request, f'Não foi possível adicionar: {exc}')
            return redirect('list_detail', pk=self.game_list.pk)
        return render(request, 'collection/form.html', {'form': form, 'list': self.game_list})


class GameListItemUpdateView(LoginRequiredMixin, ItemListOwnerRequiredMixin, UpdateView):
    model = GameListItem
    form_class = GameListItemForm
    pk_url_kwarg = 'item_pk'
    template_name = 'collection/form.html'
    context_object_name = 'item'

    def get_queryset(self):
        return GameListItem.objects.filter(list=self.game_list)

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Item atualizado.')
        return response

    def get_success_url(self):
        return redirect('list_detail', pk=self.game_list.pk).url

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['list'] = self.game_list
        return context


class GameListItemDeleteView(LoginRequiredMixin, ItemListOwnerRequiredMixin, DetailView):
    model = GameListItem
    pk_url_kwarg = 'item_pk'
    template_name = 'collection/form.html'
    context_object_name = 'item'
    permission_denied_message = 'Você não tem permissão para remover itens desta lista.'

    def get_queryset(self):
        return GameListItem.objects.filter(list=self.game_list)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        messages.success(request, 'Item removido.')
        return redirect('list_detail', pk=self.game_list.pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['list'] = self.game_list
        return context


class ReorderListView(View):
    def post(self, request, list_pk, *args, **kwargs):
        data = json.loads(request.body)
        order = data.get('order', [])
        for index, item_id in enumerate(order):
            GameListItem.objects.filter(pk=item_id, list_id=list_pk).update(order=index)
        return JsonResponse({'status': 'ok'})
