from django.contrib.auth.forms import AuthenticationForm
from django import forms
from .models import Serie, Turma, Disciplina

class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class SerieForm(forms.ModelForm):
    class Meta:
        model = Serie
        fields = ['nome']

class TurmaForm(forms.ModelForm):
    class Meta:
        model = Turma
        fields = ['nome', 'serie']

class DisciplinaForm(forms.ModelForm):
    class Meta:
        model = Disciplina
        fields = ['nome', 'turma', 'professor']