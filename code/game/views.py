import os
import requests
from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from game.models import Game, UserGameList
from joystickjuice.utils import STATUS_CHOICES
from game.forms import GameStatusForm, GameForm
from review.models import Review
from django.db.models import Avg, Count

User = get_user_model()

# Integração IGDB
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

def get_igdb_token():
    url = "https://id.twitch.tv/oauth2/token"
    params = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "client_credentials"
    }
    resp = requests.post(url, params=params)
    resp.raise_for_status()
    return resp.json()["access_token"]

# Add
def fetch_and_save(request):
    """Busca jogo na IGDB e salva no banco"""
    if request.method == "POST":
        game_name = request.POST.get("nome")
        token = get_igdb_token()

        headers = {
            "Client-ID": CLIENT_ID,
            "Authorization": f"Bearer {token}"
        }

        body = f'''
            search "{game_name}";
            fields name, genres.name, first_release_date, summary, involved_companies.company.name, cover.url, artworks.url, videos.video_id;
            limit 1;
        '''

        response = requests.post(
            "https://api.igdb.com/v4/games",
            headers=headers,
            data=body
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
            if "genres" in game_data and game_data["genres"]:
                try:
                    genre = game_data["genres"][0]["name"]
                except (TypeError, KeyError):
                    genre = ""

            developer = ""
            if "involved_companies" in game_data and game_data["involved_companies"]:
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
            if "artworks" in game_data and game_data["artworks"]:
                try:
                    banner_url = game_data["artworks"][0]["url"]
                    if banner_url.startswith("//"):
                        banner_url = "https:" + banner_url
                    banner_url = banner_url.replace("t_thumb", "t_1080p")
                except (TypeError, KeyError):
                    banner_url = ""

            trailer_url = ""
            if "videos" in game_data and game_data["videos"]:
                try:
                    video_id = game_data["videos"][0]["video_id"]
                    trailer_url = f"https://www.youtube.com/embed/{video_id}?rel=0&modestbranding=1&enablejsapi=1"
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
                trailer_url=trailer_url
            )
            new_game.save()
            messages.success(request, f"Jogo '{new_game.title}' adicionado com sucesso.")

        return redirect("list_game")

    return render(request, "game/fill.html")

# Read
def list_games(request):
    query = request.GET.get("q", "").strip()
    games = Game.objects.all()

    if query:
        filtered_games = games.filter(title__icontains=query)
    else:
        filtered_games = games

    show_create_button = query and not filtered_games.exists()

    context = {
        "games": filtered_games,
        "query": query,
        "show_create_button": show_create_button,
    }

    return render(request, "game/list.html", context)

#Create
@login_required
def create_game(request):
    if request.method == "POST":
        form = GameForm(request.POST)
        if form.is_valid():
            game = form.save()
            messages.success(request, f"Jogo '{game.title}' criado com sucesso!")
            return redirect("list_game")
    else:
        form = GameForm()

    return render(request, "game/form.html", {
        "form": form,
        "game": None,
        "action": "create"
    })

#Update
@login_required
def edit_game(request, pk):
    game = get_object_or_404(Game, pk=pk)

    if request.method == "POST":
        form = GameForm(request.POST, instance=game)
        if form.is_valid():
            form.save()
            messages.success(request, f"Jogo '{game.title}' atualizado com sucesso!")
            return redirect("list_game")
    else:
        form = GameForm(instance=game)

    return render(request, "game/form.html", {
        "form": form,
        "game": game,
        "action": "edit"
    })

#Delete
@login_required
def delete_game(request, pk):
    game = get_object_or_404(Game, pk=pk)

    if request.method == "POST":
        title = game.title
        game.delete()
        messages.success(request, f"Jogo '{title}' removido com sucesso!")
        return redirect("list_game")

    return render(request, "game/form.html", {
        "game": game,
        "action": "delete"
    })

# Detail
def game_detail(request, game_id):
    game = get_object_or_404(Game, pk=game_id)
    user = request.user

    in_list = False
    user_status = None
    is_favorite = False
    is_liked = False

    if user.is_authenticated:
        ug = UserGameList.objects.filter(user=user, game=game).first()
        if ug:
            in_list = True
            user_status = ug.status
        else:
            user_status = "P"

        is_favorite = user in game.favorites.all()
        is_liked = user in game.likes.all()

        status_form = GameStatusForm(initial={'status': user_status})
    else:
        status_form = None

    reviews_qs = Review.objects.filter(game=game).select_related('user').order_by('-created_at')
    reviews_count = reviews_qs.count()
    avg_rating = reviews_qs.aggregate(avg=Avg('rating'))['avg'] or 0

    user_review = None
    review_exists = False
    if user.is_authenticated:
        user_review = reviews_qs.filter(user=user).first()
        review_exists = user_review is not None

    context = {
    "game": game,
    "in_list": in_list,
    "user_status": user_status,
    "is_favorite": is_favorite,
    "is_liked": is_liked,
    "status_form": status_form,
    "avg_rating": avg_rating,
    "reviews_count": reviews_count,
    "review_exists": review_exists,
    "user_review": user_review,
}

    return render(request, "game/detail.html", context)

# User Game List
@login_required
def user_game_list(request, pk=None):
    if pk:
        user_profile = get_object_or_404(User, pk=pk)
    else:
        user_profile = request.user

    qs = UserGameList.objects.filter(user=user_profile)
    status = request.GET.get("status")
    if status and status != "T":
        qs = qs.filter(status=status)

    context = {
        "user_games": qs,
        "user_profile": user_profile,
        "current_status": status or "T",
    }
    return render(request, "games/user_game_list.html", context)

# Add to List
@login_required
def add_to_list(request, game_id):
    game = get_object_or_404(Game, pk=game_id)
    user = request.user

    ug = UserGameList.objects.filter(user=user, game=game).first()
    if ug:
        messages.info(request, f"'{game.title}' já está na sua lista.")
    else:
        ug = UserGameList(user=user, game=game, status="P")
        ug.save()
        messages.success(request, f"'{game.title}' adicionado à sua lista (Para jogar).")
    return redirect(request.META.get("HTTP_REFERER", "/"))

# Update Game Status
@login_required
def update_game_status(request, game_id):
    if request.method == "POST":
        status = request.POST.get("status")
        if status not in dict(STATUS_CHOICES):
            messages.error(request, "Status inválido.")
            return redirect(request.META.get("HTTP_REFERER", "/"))

        user = request.user
        ug = UserGameList.objects.filter(user=user, game_id=game_id).first()

        if ug:
            ug.status = status
            ug.save()
            messages.success(request, f"Status de '{ug.game.title}' atualizado para {ug.get_status_display()}.")
        else:
            ug = UserGameList(user=user, game_id=game_id, status=status)
            ug.save()
            messages.success(request, f"'{ug.game.title}' adicionado à sua lista com status {ug.get_status_display()}.")

    return redirect(request.META.get("HTTP_REFERER", "/"))

# Remove from List
@login_required
def remove_from_list(request, game_id):
    user = request.user
    ug = UserGameList.objects.filter(user=user, game_id=game_id).first()
    if ug:
        ug.delete()
        messages.success(request, "Jogo removido da sua lista.")
    else:
        messages.info(request, "Jogo não estava na sua lista.")
    return redirect(request.META.get("HTTP_REFERER", "/"))

# Toggle Favorite
@login_required
def toggle_favorite(request, game_id):
    user = request.user
    game = get_object_or_404(Game, pk=game_id)

    if user in game.favorites.all():
        game.favorites.remove(user)
        messages.info(request, f"'{game.title}' removido dos favoritos.")
    else:
        game.favorites.add(user)
        messages.success(request, f"'{game.title}' adicionado aos favoritos!")

    return redirect(request.META.get("HTTP_REFERER", "/"))

# Toggle Like
@login_required
def toggle_like(request, game_id):
    user = request.user
    game = get_object_or_404(Game, pk=game_id)

    if user in game.likes.all():
        game.likes.remove(user)
        messages.info(request, f"Você retirou o like de '{game.title}'.")
    else:
        game.likes.add(user)
        messages.success(request, f"Você curtiu '{game.title}'!")

    return redirect(request.META.get("HTTP_REFERER", "/"))