from django import forms
from django.contrib.auth.models import User
from .models import Usuario, Escola, Aluno
from django.shortcuts import get_object_or_404
from django.utils import timezone


class CadastroForm(forms.Form):
    nome = forms.CharField(label='Nome', widget=forms.TextInput(attrs={'placeholder': 'Ex: João da Silva'}))
    username = forms.CharField(label='Nome de Usuário', widget=forms.TextInput(attrs={'placeholder': 'Ex: jsilva'}))
    password = forms.CharField(widget=forms.PasswordInput(), label='Senha')
    confirm_password = forms.CharField(widget=forms.PasswordInput(), label='Confirmar Senha')
    escola_existente = forms.ModelChoiceField(queryset=Escola.objects.all(), label='Escola Existente', required=False)

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("As senhas não coincidem.")

    def save(self):
        user = User.objects.create_user(username=self.cleaned_data['username'], password=self.cleaned_data['password'])
        usuario = Usuario(user=user, nome=self.cleaned_data['nome'])
        if self.cleaned_data.get('escola_existente'):
            usuario.escola = self.cleaned_data['escola_existente']
        usuario.save()
        return usuario


class EscolaForm(forms.Form):
    nome = forms.CharField(label='Nome', widget=forms.TextInput(attrs={'placeholder': 'Ex: E.E. Monteiro Lobato'}))
    email = forms.CharField(label='Email', widget=forms.TextInput(attrs={'placeholder': 'Ex: escola@escola.com.br'}))
    endereco = forms.CharField(label='Endereço', widget=forms.TextInput(attrs={'placeholder': 'Ex: rua monteiro Lobato'}))

    def saveEscola(self):
        nome_escola = self.cleaned_data['nome']
        try:
            escola_existente = Escola.objects.get(nome=nome_escola)
            return escola_existente
        except Escola.DoesNotExist:
            escola = Escola(
                nome=nome_escola,
                email=self.cleaned_data['email'],
                endereco=self.cleaned_data['endereco']
            )
            escola.save()
            return escola

class AlunoForm(forms.Form):
    nome = forms.CharField(label='Nome do Aluno', widget=forms.TextInput(attrs={'placeholder': 'Ex: João'}))
    idade = forms.IntegerField(label='Idade', widget=forms.TextInput(attrs={'placeholder': 'Ex: 18'}))
    Aluno_existente = forms.ModelChoiceField(queryset=Aluno.objects.all(), label='Questionário Existente', required=False)

    def save(self, usuario):
        if self.cleaned_data.get('Aluno_existente'):
            return self.cleaned_data['Aluno_existente']
        else:
            nome = self.cleaned_data['nome']
            idade = self.cleaned_data['idade']
            aluno = Aluno(nome=nome, idade=idade, usuario=usuario)
            aluno.save()
            return aluno