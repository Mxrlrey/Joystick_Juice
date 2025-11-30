import datetime

from django import forms
from django.contrib.auth.models import User
from .models import Person


class SignupForm(forms.Form):
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


        if User.objects.filter(username=cleaned_data.get("username")).exists():
            raise forms.ValidationError("Este nome de usuário já está em uso.")

        if User.objects.filter(email=cleaned_data.get("email")).exists():
            raise forms.ValidationError("Este email já está em uso.")

        return cleaned_data

    def save(self):
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password']
        )
        Person.objects.create(user=user)
        return user


class PersonForm(forms.ModelForm):
    birthdate = forms.DateField(required=False, widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date',}, format='%Y-%m-%d'), input_formats=['%Y-%m-%d', '%d/%m/%Y'])

    class Meta:
        model = Person
        fields = ['name', 'birthdate', 'gender', 'bio']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            
            'gender': forms.Select(attrs={'class': 'form-select form-control'}),
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
        widgets = {
            'avatar_url': forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
        }


class UserDeleteForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']  

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.disabled = True
            field.widget.attrs['class'] = 'form-control' 