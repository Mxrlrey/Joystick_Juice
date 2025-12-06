from django import forms
from .models import Review, Comment
from joystickjuice.utils import RATING_CHOICES


class ReviewForm(forms.ModelForm):
    rating = forms.TypedChoiceField(
        choices=RATING_CHOICES,
        coerce=float,
        widget=forms.Select(attrs={'class': 'form-select form-select-lg'})
    )
    comment = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3, 'class': 'form-control form-control-lg'})
    )


    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 3}),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['opinion']
        widgets = {
            'opinion': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }