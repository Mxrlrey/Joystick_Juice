from django import forms
from .models import Club, ClubMessage
from game.models import Game


class ClubForm(forms.ModelForm):
    class Meta:
        model = Club
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Nome do clube'}),
            'description': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Descrição do clube'}),
        }

class ClubMessageForm(forms.ModelForm):
    game = forms.ModelChoiceField(
        queryset=Game.objects.all(),
        required=False,
        empty_label="Nenhum jogo selecionado"
    )

    class Meta:
        model = ClubMessage
        fields = ['content', 'game']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Digite sua mensagem aqui...'})
        }