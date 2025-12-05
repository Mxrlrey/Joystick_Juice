from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Review
from .forms import ReviewForm
from game.models import Game
from django.db.models import Avg

@login_required
def create_review(request, game_id):

    game = get_object_or_404(Game, pk=game_id)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.game = game
            review.save()
            messages.success(request, "Avaliação criada com sucesso.")
            return redirect('game_detail', game.pk)
    else:
        form = ReviewForm()

    return render(request, "review/form.html", {
        "form": form,
        "game": game,
        "review": None
    })


def list_reviews(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    reviews = Review.objects.filter(game=game).order_by('-created_at')
    avg_rating = reviews.aggregate(avg=Avg('rating'))['avg'] or 0

    return render(request, 'review/list.html', {
        'game': game,
        'reviews': reviews,
        'avg_rating': avg_rating
    })

def review_detail(request, pk):
    review = get_object_or_404(Review, pk=pk)
    return render(request, 'review/detail.html', {'review': review})

@login_required
def edit_review(request, pk):
 
    review = get_object_or_404(Review, pk=pk)

    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            messages.success(request, "Avaliação atualizada com sucesso.")
            return redirect('detail_review', pk=pk)
    else:
        form = ReviewForm(instance=review)

    return render(request, "review/form.html", {
    "form": form,
    "review": review,
    })

@login_required
def delete_review(request, pk):

    review = get_object_or_404(Review, pk=pk)

    if request.method == 'POST':
        game_id = review.game.pk
        review.delete()
        messages.success(request, "Avaliação removida.")
        return redirect('game_detail', game_id=game_id)

    return render(request, "review/form.html", {
    "review": review,
    })