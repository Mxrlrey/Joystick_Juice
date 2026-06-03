from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Avg
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import CreateView, DetailView, ListView, UpdateView, View

from game.models import Game
from review.forms import CommentForm, ReviewForm
from review.models import Comment, Review


class ReviewCreateView(LoginRequiredMixin, CreateView):
    model = Review
    form_class = ReviewForm
    template_name = "review/form.html"

    def dispatch(self, request, *args, **kwargs):
        self.game = get_object_or_404(Game, pk=kwargs["game_id"])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.game = self.game
        self.object = form.save()
        return redirect("game_detail", self.game.pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({"game": self.game, "review": None})
        return context


class ReviewListView(ListView):
    template_name = "review/list.html"
    context_object_name = "reviews"

    def dispatch(self, request, *args, **kwargs):
        self.game = get_object_or_404(Game, id=kwargs["game_id"])
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Review.objects.filter(game=self.game).order_by("-created_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["game"] = self.game
        context["avg_rating"] = self.object_list.aggregate(avg=Avg("rating"))["avg"] or 0
        return context


class ReviewDetailView(DetailView):
    model = Review
    pk_url_kwarg = "pk"
    template_name = "review/detail.html"
    context_object_name = "review"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["comments"] = Comment.objects.filter(review=self.object).order_by("-created_at")
        context["form"] = CommentForm()
        return context


class ReviewUpdateView(LoginRequiredMixin, UpdateView):
    model = Review
    form_class = ReviewForm
    pk_url_kwarg = "pk"
    template_name = "review/form.html"
    context_object_name = "review"

    def get_success_url(self):
        return self.object.get_absolute_url() if hasattr(self.object, "get_absolute_url") else None

    def form_valid(self, form):
        self.object = form.save()
        return redirect("detail_review", pk=self.object.pk)


class ReviewDeleteView(LoginRequiredMixin, DetailView):
    model = Review
    pk_url_kwarg = "pk"
    template_name = "review/form.html"
    context_object_name = "review"

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        game_id = self.object.game.pk
        self.object.delete()
        return redirect("game_detail", game_id=game_id)


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = "review/comment_form.html"

    def dispatch(self, request, *args, **kwargs):
        self.review = get_object_or_404(Review, pk=kwargs["review_id"])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.review = self.review
        self.object = form.save()
        return redirect("detail_review", self.review.pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["review"] = self.review
        return context


class CommentListView(ListView):
    template_name = "review/comment_list.html"
    context_object_name = "comments"

    def dispatch(self, request, *args, **kwargs):
        self.review = get_object_or_404(Review, pk=kwargs["review_id"])
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Comment.objects.filter(review=self.review).order_by("-created_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["review"] = self.review
        return context


class CommentOwnerMixin(UserPassesTestMixin):
    def test_func(self):
        return self.get_object().user == self.request.user

    def handle_no_permission(self):
        return redirect("detail_review", self.get_object().review.pk)


class CommentUpdateView(LoginRequiredMixin, CommentOwnerMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    pk_url_kwarg = "pk"
    template_name = "review/comment_form.html"
    context_object_name = "comment"

    def form_valid(self, form):
        self.object = form.save()
        return redirect("detail_review", self.object.review.pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({"review": self.object.review, "edit": True})
        return context


class CommentDeleteView(LoginRequiredMixin, CommentOwnerMixin, DetailView):
    model = Comment
    pk_url_kwarg = "pk"
    template_name = "review/comment_form.html"
    context_object_name = "comment"

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        review_pk = self.object.review.pk
        self.object.delete()
        return redirect("detail_review", review_pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = CommentForm(instance=self.object)
        for field in form.fields.values():
            field.disabled = True
        context.update({"form": form, "review": self.object.review, "delete": True})
        return context
