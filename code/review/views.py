from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import Review, Comment
from .forms import ReviewForm, CommentForm
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
    comments = Comment.objects.filter(review=review).order_by('-created_at')
    form = CommentForm()
    return render(request, 'review/detail.html', {'review': review, 'comments': comments, 'form': form})

@login_required
def edit_review(request, pk):
 
    review = get_object_or_404(Review, pk=pk)

    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
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
        return redirect('game_detail', game_id=game_id)

    return render(request, "review/form.html", {
    "review": review,
    })

@login_required
def create_comment(request, review_id):

    review = get_object_or_404(Review, pk=review_id)
    
    if request.method == 'POST':
        form = CommentForm(request.POST)  
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.review = review
            comment.save()
            return redirect('detail_review', review.pk)
    else:
        form = CommentForm()

    return render(request, 'review/comment_form.html', {
        'form': form,
        'review': review,
    })


def comment_list(request, review_id):
    review = get_object_or_404(Review, pk=review_id)
    comments = Comment.objects.filter(review=review).order_by('-created_at')
    return render(request, 'review/comment_list.html', {
        'review': review,
        'comments': comments,
    })

@login_required
def edit_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)

    if comment.user != request.user:
        return redirect('detail_review', comment.review.pk)

    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save() 
            return redirect('detail_review', comment.review.pk)
    else:
        form = CommentForm(instance=comment)

    return render(request, 'review/comment_form.html', {
        'form': form,
        'comment': comment,
        'review': comment.review,
        'edit': True,
    })

@login_required
def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    
    if comment.user != request.user:
        return redirect('detail_review', comment.review.pk)

    if request.method == 'POST':
        review_pk = comment.review.pk
        comment.delete()
        return redirect('detail_review', review_pk)
    else:
        form = CommentForm(instance=comment)

    for f in form.fields.values():
        f.disabled = True

    return render(request, 'review/comment_form.html', {
        'form': form,
        'comment': comment,
        'review': comment.review,
        'delete': True,  
    })