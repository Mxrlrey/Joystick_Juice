import os
import requests
from datetime import datetime
from django.views.generic import DetailView, ListView
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from game.models import Game

User = get_user_model()

# -------------------
# Integração IGDB
# -------------------

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

def fetch_and_save(request):
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

            if Game.objects.filter(title__iexact=game_data.get("name", "")).exists():
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
                release_date = datetime.utcfromtimestamp(
                    game_data["first_release_date"]
                ).date()

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
                    trailer_url = f"https://www.youtube.com/embed/{video_id}"
                except (TypeError, KeyError):
                    trailer_url = ""

            Game.objects.create(
                title=game_data.get("name", game_name),
                genre=genre or "Indefinido",
                release_date=release_date or datetime.today().date(),
                synopsis=game_data.get("summary", ""),
                developer=developer or "Desconhecido",
                cover_url=cover_url,
                banner_url=banner_url,
                trailer_url=trailer_url
            )

        return redirect("list_game")

    return render(request, "game/fill.html")

def list_games(request):
    games = Game.objects.all()
    return render(request, 'game/list.html', {'games': games})

