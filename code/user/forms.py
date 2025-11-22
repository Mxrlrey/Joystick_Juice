from django import forms
from django.contrib.auth.models import User
from .models import Person

class SignupForm(forms.Form):
    username = forms.CharField(label="Nome de usuário", max_length=20)
    email = forms.EmailField(label="Email")
    password = forms.CharField(label="Senha", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirmar senha", widget=forms.PasswordInput)

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


class LoginForm(forms.Form):
    email = forms.EmailField(label="Email")
    password = forms.CharField(widget=forms.PasswordInput, label="Senha")

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")

        if email and password:
            from django.contrib.auth.models import User
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                raise forms.ValidationError("Email ou senha inválidos")

            user = authenticate(username=user.username, password=password)
            if user is None:
                raise forms.ValidationError("Email ou senha inválidos")

            cleaned_data['user'] = user
        return cleaned_data