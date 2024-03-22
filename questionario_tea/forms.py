from django import forms
from django.contrib.auth.models import User
from .models import Aluno
from .models import Resposta

class CadastroForm(forms.Form):
    username = forms.CharField(label='Nome de Usuário')
    password = forms.CharField(widget=forms.PasswordInput(), label='Senha')
    confirm_password = forms.CharField(widget=forms.PasswordInput(), label='Confirmar Senha')
    nome = forms.CharField(label='Nome')
    cpf_rg = forms.CharField(label='CPF ou RG')
    idade = forms.IntegerField(label='Idade', required=False)
    endereco = forms.CharField(label='Endereço')
    nome_responsavel = forms.CharField(label='Nome do Responsável')

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("As senhas não coincidem.")

    def save(self):
        user = User.objects.create_user(username=self.cleaned_data['username'], password=self.cleaned_data['password'])
        aluno = Aluno(user=user, nome=self.cleaned_data['nome'], cpf_rg=self.cleaned_data['cpf_rg'],
                      idade=self.cleaned_data['idade'], endereco=self.cleaned_data['endereco'],
                      nome_responsavel=self.cleaned_data['nome_responsavel'])
        aluno.save()