from django import forms
from .models import GameList, GameListItem

class GameListForm(forms.ModelForm):
    class Meta:
        model = GameList
        fields = ['name', 'description', 'is_public']

class GameListItemForm(forms.ModelForm):
    class Meta:
        model = GameListItem
        fields = ['game', 'note', 'order']