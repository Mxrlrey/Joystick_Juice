import datetime

from django import forms
from django.contrib.auth.models import User
from .models import Person


class SignupForm(forms.Form):
    # Aplicando o widget para adicionar a classe 'form-control'
    username = forms.CharField(
        label="Nome de usuário",
        max_length=20,
        widget=forms.TextInput(attrs={'class': 'form-control'}) 
    )
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        label="Senha",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    password2 = forms.CharField(
        label="Confirmar senha",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password2 = cleaned_data.get("password2")

        if password != password2:
            raise forms.ValidationError("As senhas não coincidem.")

        # Verifica se username já existe
        if User.objects.filter(username=cleaned_data.get("username")).exists():
            raise forms.ValidationError("Este nome de usuário já está em uso.")
        # Verifica se email já existe
        if User.objects.filter(email=cleaned_data.get("email")).exists():
            raise forms.ValidationError("Este email já está em uso.")

        return cleaned_data

    def save(self):
        # Cria o User
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password']
        )
        # Cria a Person vinculada sem outros campos
        Person.objects.create(user=user)
        return user


class PersonForm(forms.ModelForm):

    class Meta:
        model = Person
        fields = ['name', 'birthdate', 'gender', 'bio']
        # Usando 'widgets' para aplicar a classe 'form-control' aos campos do ModelForm
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'birthdate': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}), # type='date' para melhor UX em navegadores
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        birthdate = cleaned_data.get("birthdate")

        if birthdate:
            if birthdate > datetime.date.today():
                raise forms.ValidationError("Data invalida")

        return cleaned_data


class AvatarForm(forms.ModelForm):

    class Meta:
        model = Person
        fields = ['avatar_url']
        # Aplicando a classe 'form-control' via 'widgets'
        widgets = {
            'avatar_url': forms.URLInput(attrs={'class': 'form-control'}),
        }


class UserDeleteForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']  
        # NOTA: O 'form-control' será aplicado no __init__ desta classe
        # (onde os campos também são desabilitados).

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # O loop aplica 'disabled = True' E 'class = form-control'
        for field in self.fields.values():
            field.disabled = True
            field.widget.attrs['class'] = 'form-control' # Aplica 'form-control' aqui