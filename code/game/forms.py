from django import forms
from joystickjuice.utils import STATUS_CHOICES
from game.models import Game
import re

class GameStatusForm(forms.Form):
    status = forms.ChoiceField(
        choices=STATUS_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select w-auto'})
    )

class GameForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ['title', 'genre', 'release_date', 'synopsis', 'developer', 'cover_url', 'banner_url', 'trailer_url']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Nome do jogo'}),
            'genre': forms.TextInput(attrs={'placeholder': 'Gênero'}),
            'release_date': forms.DateInput(attrs={'type': 'date'}),
            'synopsis': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Sinopse'}),
            'developer': forms.TextInput(attrs={'placeholder': 'Desenvolvedor'}),
            'cover_url': forms.URLInput(attrs={'placeholder': 'URL da capa'}),
            'banner_url': forms.URLInput(attrs={'placeholder': 'URL do banner'}),
            'trailer_url': forms.URLInput(attrs={'placeholder': 'URL do trailer'}),
        }

    def clean_trailer_url(self):
        url = self.cleaned_data.get('trailer_url')
        if url:
            # Regex simples para pegar o video_id do YouTube
            match = re.search(r'(?:v=|youtu\.be/)([\w-]+)', url)
            if match:
                video_id = match.group(1)
                return f'https://www.youtube.com/embed/{video_id}'
            else:
                raise forms.ValidationError("URL do YouTube inválida")
        return url
