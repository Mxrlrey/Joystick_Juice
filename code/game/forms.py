from django import forms
from joystickjuice.utils import STATUS_CHOICES

class GameStatusForm(forms.Form):
    status = forms.ChoiceField(
        choices=STATUS_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select w-auto'})
    )

