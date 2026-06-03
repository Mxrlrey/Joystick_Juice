import os
from datetime import datetime

import requests
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import Avg, Count
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, TemplateView, UpdateView, View

from game.forms import GameForm, GameStatusForm
from game.models import Game, UserGameList
from joystickjuice.utils import STATUS_CHOICES
from review.models import Review

User = get_user_model()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")


def get_igdb_token():
    url = "https://id.twitch.tv/oauth2/token"
    params = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "client_credentials",
    }
    resp = requests.post(url, params=params)
    resp.raise_for_status()
    return resp.json()["access_token"]


class RedirectBackMixin:
    default_redirect_url = "/"

    def redirect_back(self):
        return redirect(self.request.META.get("HTTP_REFERER", self.default_redirect_url))


class FetchAndSaveView(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    permission_required = "game.add_game"
    raise_exception = True
    template_name = "game/fill.html"

    def post(self, request, *args, **kwargs):
        game_name = request.POST.get("nome")
        token = get_igdb_token()

        headers = {
            "Client-ID": CLIENT_ID,
            "Authorization": f"Bearer {token}",
        }

        body = f'''
            search "{game_name}";
            fields name, genres.name, first_release_date, summary, involved_companies.company.name, cover.url, artworks.url, videos.video_id;
            limit 1;
        '''

        response = requests.post(
            "https://api.igdb.com/v4/games",
            headers=headers,
            data=body,
        )
        response.raise_for_status()
        data = response.json()

        if data:
            game_data = data[0]
            existing_game = Game.objects.filter(title__iexact=game_data.get("name", "")).first()
            if existing_game:
                messages.info(request, f"O jogo '{existing_game.title}' já existe na base.")
                return redirect("list_game")

            genre = ""
            if game_data.get("genres"):
                try:
                    genre = game_data["genres"][0]["name"]
                except (TypeError, KeyError):
                    genre = ""

            developer = ""
            if game_data.get("involved_companies"):
                try:
                    developer = game_data["involved_companies"][0]["company"]["name"]
                except (TypeError, KeyError):
                    developer = ""

            release_date = None
            if game_data.get("first_release_date"):
                release_date = datetime.utcfromtimestamp(game_data["first_release_date"]).date()

            cover_url = game_data.get("cover", {}).get("url", "")
            if cover_url and cover_url.startswith("//"):
                cover_url = "https:" + cover_url
            if cover_url:
                cover_url = cover_url.replace("t_thumb", "t_cover_big")

            banner_url = ""
            if game_data.get("artworks"):
                try:
                    banner_url = game_data["artworks"][0]["url"]
                    if banner_url.startswith("//"):
                        banner_url = "https:" + banner_url
                    banner_url = banner_url.replace("t_thumb", "t_1080p")
                except (TypeError, KeyError):
                    banner_url = ""

            trailer_url = ""
            if game_data.get("videos"):
                try:
                    video_id = game_data["videos"][0]["video_id"]
                    trailer_url = (
                        f"https://www.youtube.com/embed/{video_id}?rel=0&modestbranding=1&enablejsapi=1"
                    )
                except (TypeError, KeyError):
                    trailer_url = ""

            new_game = Game(
                title=game_data.get("name", game_name),
                genre=genre or "Indefinido",
                release_date=release_date or datetime.today().date(),
                synopsis=game_data.get("summary", ""),
                developer=developer or "Desconhecido",
                cover_url=cover_url,
                banner_url=banner_url,
                trailer_url=trailer_url,
            )
            new_game.save()
            messages.success(request, f"Jogo '{new_game.title}' adicionado com sucesso.")

        return redirect("list_game")


class GameListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = "game.change_game"
    raise_exception = True
    model = Game
    template_name = "game/list.html"
    context_object_name = "games"

    def get_queryset(self):
        query = self.request.GET.get("q", "").strip()
        queryset = Game.objects.all()
        if query:
            queryset = queryset.filter(title__icontains=query)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get("q", "").strip()
        context["query"] = query
        context["show_create_button"] = bool(query) and not context["games"].exists()
        return context


class GameCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = "game.add_game"
    raise_exception = True
    model = Game
    form_class = GameForm
    template_name = "game/form.html"
    success_url = reverse_lazy("list_game")

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f"Jogo '{self.object.title}' criado com sucesso!")
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({"game": None, "action": "create"})
        return context


class GameUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = "game.change_game"
    raise_exception = True
    model = Game
    form_class = GameForm
    pk_url_kwarg = "pk"
    template_name = "game/form.html"
    success_url = reverse_lazy("list_game")

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f"Jogo '{self.object.title}' atualizado com sucesso!")
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["action"] = "edit"
        return context


class GameDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    permission_required = "game.delete_game"
    raise_exception = True
    model = Game
    pk_url_kwarg = "pk"
    template_name = "game/form.html"
    context_object_name = "game"
    success_url = reverse_lazy("list_game")

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        title = self.object.title
        self.object.delete()
        messages.success(request, f"Jogo '{title}' removido com sucesso!")
        return redirect(self.success_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["action"] = "delete"
        return context


class GameDetailView(DetailView):
    model = Game
    pk_url_kwarg = "game_id"
    template_name = "game/detail.html"
    context_object_name = "game"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        game = self.object
        user = self.request.user

        in_list = False
        user_status = None
        is_favorite = False
        is_liked = False
        status_form = None

        if user.is_authenticated:
            user_game = UserGameList.objects.filter(user=user, game=game).first()
            if user_game:
                in_list = True
                user_status = user_game.status
            else:
                user_status = "P"

            is_favorite = user in game.favorites.all()
            is_liked = user in game.likes.all()
            status_form = GameStatusForm(initial={"status": user_status})

        reviews_qs = Review.objects.filter(game=game).select_related("user").order_by("-created_at")
        user_review = reviews_qs.filter(user=user).first() if user.is_authenticated else None

        context.update(
            {
                "in_list": in_list,
                "user_status": user_status,
                "is_favorite": is_favorite,
                "is_liked": is_liked,
                "status_form": status_form,
                "avg_rating": reviews_qs.aggregate(avg=Avg("rating"))["avg"] or 0,
                "reviews_count": reviews_qs.count(),
                "review_exists": user_review is not None,
                "user_review": user_review,
            }
        )
        return context


class UserGameListView(LoginRequiredMixin, TemplateView):
    template_name = "game/user_game_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_profile = (
            get_object_or_404(User, pk=self.kwargs["pk"])
            if self.kwargs.get("pk")
            else self.request.user
        )
        is_owner = self.request.user == user_profile
        status_map = dict(STATUS_CHOICES)
        status_filters = [("T", "Todos")] + list(STATUS_CHOICES)
        queryset = UserGameList.objects.filter(user=user_profile).select_related("game")
        query = self.request.GET.get("q", "").strip()
        status_filter = self.request.GET.get("status", "T").strip()

        if query:
            queryset = queryset.filter(game__title__icontains=query)

        if status_filter != "T" and status_filter in status_map:
            queryset = queryset.filter(status=status_filter)

        if query:
            ordered_games = {
                "S": {
                    "name": f'Resultados para "{query}"',
                    "games": list(queryset),
                }
            }
        else:
            games_by_status = {
                code: {"name": name, "games": []}
                for code, name in STATUS_CHOICES
            }
            for user_game in queryset.order_by("updated_at"):
                if user_game.status in games_by_status:
                    games_by_status[user_game.status]["games"].append(user_game)

            display_order = ["J", "P", "C", "A"]
            ordered_games = {
                code: games_by_status[code]
                for code in display_order
                if games_by_status[code]["games"]
            }

        context.update(
            {
                "user_games_grouped": ordered_games,
                "STATUS_FILTERS": status_filters,
                "query": query,
                "current_status": status_filter,
                "user_profile": user_profile,
                "STATUS_CHOICES": STATUS_CHOICES,
                "is_owner": is_owner,
            }
        )
        return context


class AddToListView(LoginRequiredMixin, RedirectBackMixin, View):
    def post(self, request, game_id, *args, **kwargs):
        game = get_object_or_404(Game, pk=game_id)
        user_game = UserGameList.objects.filter(user=request.user, game=game).first()
        if user_game:
            messages.info(request, f"'{game.title}' já está na sua lista.")
        else:
            UserGameList.objects.create(user=request.user, game=game, status="P")
            messages.success(request, f"'{game.title}' adicionado à sua lista (Para jogar).")
        return self.redirect_back()


class UpdateGameStatusView(LoginRequiredMixin, RedirectBackMixin, View):
    def post(self, request, game_id, *args, **kwargs):
        status = request.POST.get("status")
        if status not in dict(STATUS_CHOICES):
            messages.error(request, "Status inválido.")
            return self.redirect_back()

        user_game = UserGameList.objects.filter(user=request.user, game_id=game_id).first()
        if user_game:
            user_game.status = status
            user_game.save()
            messages.success(
                request,
                f"Status de '{user_game.game.title}' atualizado para {user_game.get_status_display()}.",
            )
        else:
            user_game = UserGameList.objects.create(user=request.user, game_id=game_id, status=status)
            messages.success(
                request,
                f"'{user_game.game.title}' adicionado à sua lista com status {user_game.get_status_display()}.",
            )
        return self.redirect_back()


class RemoveFromListView(LoginRequiredMixin, RedirectBackMixin, View):
    def post(self, request, game_id, *args, **kwargs):
        user_game = UserGameList.objects.filter(user=request.user, game_id=game_id).first()
        if user_game:
            user_game.delete()
            messages.success(request, "Jogo removido da sua lista.")
        else:
            messages.info(request, "Jogo não estava na sua lista.")
        return self.redirect_back()


class ToggleFavoriteView(LoginRequiredMixin, RedirectBackMixin, View):
    def post(self, request, game_id, *args, **kwargs):
        game = get_object_or_404(Game, pk=game_id)
        if request.user in game.favorites.all():
            game.favorites.remove(request.user)
            messages.info(request, f"'{game.title}' removido dos favoritos.")
        else:
            game.favorites.add(request.user)
            messages.success(request, f"'{game.title}' adicionado aos favoritos!")
        return self.redirect_back()


class ToggleLikeView(LoginRequiredMixin, RedirectBackMixin, View):
    def post(self, request, game_id, *args, **kwargs):
        game = get_object_or_404(Game, pk=game_id)
        if request.user in game.likes.all():
            game.likes.remove(request.user)
            messages.info(request, f"Você retirou o like de '{game.title}'.")
        else:
            game.likes.add(request.user)
            messages.success(request, f"Você curtiu '{game.title}'!")
        return self.redirect_back()


class HomePageView(TemplateView):
    template_name = "game/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        top_rated_games = Game.objects.annotate(
            avg_rating=Avg("review__rating"),
            list_count=Count("usergamelist"),
        ).filter(avg_rating__isnull=False).order_by("-avg_rating", "-list_count")[:10]

        popular_games_qs = Game.objects.annotate(list_count=Count("usergamelist")).order_by("-list_count")
        popular_games = popular_games_qs[:10]
        if not popular_games.exists():
            popular_games = Game.objects.all().order_by("?")[:10]

        context.update(
            {
                "top_rated_games": top_rated_games,
                "popular_games": popular_games,
                "recent_games": Game.objects.all().order_by("-release_date")[:10],
                "all_games": Game.objects.all(),
            }
        )
        return context
