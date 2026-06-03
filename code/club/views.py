from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView, View

from club.forms import ClubForm, ClubMessageForm
from club.models import Club


class ClubCreatorRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user == self.get_object().creator

    def handle_no_permission(self):
        messages.error(self.request, 'Somente o criador pode editar este clube.')
        return redirect('list_clubs')


class ClubCreateView(LoginRequiredMixin, CreateView):
    model = Club
    form_class = ClubForm
    template_name = 'club/form.html'

    def form_valid(self, form):
        form.instance.creator = self.request.user
        response = super().form_valid(form)
        self.object.members.add(self.request.user)
        messages.success(self.request, f'Clube "{self.object.name}" criado com sucesso!')
        return response

    def get_success_url(self):
        return reverse_lazy('list_clubs')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'create'
        return context


class ClubListView(LoginRequiredMixin, ListView):
    model = Club
    template_name = 'club/list.html'
    context_object_name = 'clubs'


class ClubUpdateView(LoginRequiredMixin, ClubCreatorRequiredMixin, UpdateView):
    model = Club
    form_class = ClubForm
    pk_url_kwarg = 'club_id'
    template_name = 'club/form.html'
    context_object_name = 'club'

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f'Clube "{self.object.name}" atualizado com sucesso!')
        return response

    def get_success_url(self):
        return reverse_lazy('list_clubs')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'edit'
        return context


class ClubDeleteView(LoginRequiredMixin, ClubCreatorRequiredMixin, DetailView):
    model = Club
    pk_url_kwarg = 'club_id'
    template_name = 'club/form.html'
    context_object_name = 'club'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        club_name = self.object.name
        self.object.delete()
        messages.success(request, f'Clube "{club_name}" excluído com sucesso!')
        return redirect('list_clubs')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'delete'
        return context


class ClubDetailView(LoginRequiredMixin, DetailView):
    model = Club
    pk_url_kwarg = 'club_id'
    template_name = 'club/detail.html'
    context_object_name = 'club'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['members'] = self.object.members.all()
        return context


class JoinClubView(LoginRequiredMixin, View):
    def get(self, request, club_id, *args, **kwargs):
        club = get_object_or_404(Club, id=club_id)
        if request.user in club.members.all():
            messages.info(request, 'Você já é membro deste clube.')
        else:
            club.members.add(request.user)
            messages.success(request, f'Você entrou no clube "{club.name}".')
        return redirect('list_clubs')


class ClubChatView(LoginRequiredMixin, DetailView):
    model = Club
    pk_url_kwarg = 'club_id'
    template_name = 'club/chat.html'
    context_object_name = 'club'

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if request.user not in self.object.members.all():
            messages.error(request, 'Você precisa ser membro do clube para ver as mensagens.')
            return redirect('club_detail', club_id=self.object.id)
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = ClubMessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.club = self.object
            message.sender = request.user
            message.save()
            return redirect('club_chat', club_id=self.object.id)
        context = self.get_context_data(form=form)
        from django.shortcuts import render
        return render(request, self.template_name, context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = kwargs.get('form') or ClubMessageForm()
        context['messages_list'] = self.object.messages.all()
        return context


class UserClubListView(LoginRequiredMixin, ListView):
    template_name = 'club/list.html'
    context_object_name = 'clubs'

    def dispatch(self, request, *args, **kwargs):
        self.target_user = get_object_or_404(User, id=kwargs['user_id'])
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Club.objects.filter(members=self.target_user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'target_user': self.target_user,
            'is_owner': self.request.user == self.target_user,
            'page_title': f'Clubes de @{self.target_user.username}',
        })
        return context


class LeaveClubView(LoginRequiredMixin, View):
    def get(self, request, club_id, *args, **kwargs):
        club = get_object_or_404(Club, id=club_id)
        if request.user == club.creator:
            messages.error(
                request,
                'O criador do clube não pode sair diretamente. Transfira a propriedade ou exclua o clube.',
            )
            return redirect('club_detail', club_id=club.id)

        if request.user in club.members.all():
            club.members.remove(request.user)
            messages.success(request, f'Você saiu do clube "{club.name}".')
            return redirect('list_clubs')

        messages.info(request, 'Você não é membro deste clube.')
        return redirect('club_detail', club_id=club.id)
