from django import forms
from .models import GameList, GameListItem

class GameListForm(forms.ModelForm):
    class Meta:
        model = GameList
        fields = ['name', 'description', 'is_public']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'is_public': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class GameListItemForm(forms.ModelForm):
    class Meta:
        model = GameListItem
        fields = ['game']
        widgets = {
            'game': forms.Select(attrs={'class': 'form-control'}),
        }