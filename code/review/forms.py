from django import forms
from .models import Review

RATING_CHOICES = [
    (0.5, '0.5'),
    (1, '1'),
    (1.5, '1.5'),
    (2, '2'),
    (2.5, '2.5'),
    (3, '3'),
    (3.5, '3.5'),
    (4, '4'),
    (4.5, '4.5'),
    (5, '5'),
]

class ReviewForm(forms.ModelForm):
    rating = forms.TypedChoiceField(
    choices=RATING_CHOICES,
    coerce=float
    )

    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 3}),
        }