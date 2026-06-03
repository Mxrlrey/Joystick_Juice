from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, FormView, TemplateView, UpdateView, View

from club.models import Club
from collection.models import GameList
from game.models import UserGameList
from review.models import Review
from user.forms import AvatarForm, PersonForm, SignupForm, UserDeleteForm
from user.models import Person


class SignupView(FormView):
    form_class = SignupForm
    template_name = 'registration/signup.html'

    def form_valid(self, form):
        form.save()
        return redirect('login')


class AccountDetailView(LoginRequiredMixin, TemplateView):
    template_name = 'account/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id = self.kwargs.get('user_id')
        user_obj = get_object_or_404(User, pk=user_id) if user_id is not None else self.request.user

        try:
            person = user_obj.person
        except Exception:
            person = None

        status_counts_qs = UserGameList.objects.filter(user=user_obj).values('status').annotate(total=Count('id'))
        status_counts = {item['status']: item['total'] for item in status_counts_qs}

        context.update({
            'person': person,
            'user_obj': user_obj,
            'is_owner': self.request.user.is_authenticated and self.request.user.pk == user_obj.pk,
            'favorite_games': user_obj.favorite_games.all(),
            'status_counts': status_counts,
            'club_count': Club.objects.filter(members=user_obj).count(),
            'list_count': GameList.objects.filter(owner=user_obj).count(),
        })
        return context


class AccountDeleteView(LoginRequiredMixin, TemplateView):
    template_name = 'account/form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'form': UserDeleteForm(instance=self.request.user), 'delete': True, 'user': self.request.user})
        return context

    def post(self, request, *args, **kwargs):
        request.user.delete()
        return redirect('account_signup')


class AccountProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Person
    form_class = PersonForm
    template_name = 'account/form.html'

    def get_object(self, queryset=None):
        return self.request.user.person

    def get_success_url(self):
        return reverse_lazy('account_detail_self')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'user': self.request.user, 'edit_profile': True})
        return context


class AccountAvatarUpdateView(LoginRequiredMixin, UpdateView):
    model = Person
    form_class = AvatarForm
    template_name = 'account/edit_avatar.html'

    def get_object(self, queryset=None):
        return self.request.user.person

    def get_success_url(self):
        return reverse_lazy('account_detail_self')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'user': self.request.user, 'person': self.request.user.person})
        return context
