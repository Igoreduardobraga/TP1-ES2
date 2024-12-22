from django import forms
from .models import Post
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Comentario


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']


class RegistroForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text='Campo obrigatório.')

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ['conteudo']
        widgets = {
            'conteudo': forms.Textarea(attrs={'rows': 3, 'class': 'form-control', 'placeholder': 'Escreva seu comentário'}),
        }
