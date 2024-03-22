from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from .models import Aluno, Pergunta, Resposta
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from .forms import CadastroForm

def questionario(request):
    if request.method == 'POST':
        respostas = {}
        for key, value in request.POST.items():
            if key.startswith('pergunta_'):
                pergunta_id = int(key.split('_')[1])
                resposta_id = int(value)
                respostas[pergunta_id] = resposta_id

        aluno, created = Aluno.objects.get_or_create(user=request.user)
        processar_respostas(aluno, respostas)

        return redirect('resultado')

    perguntas = Pergunta.objects.all()
    contexto = {'perguntas': perguntas}
    return render(request, 'questionario.html', contexto)

def processar_respostas(aluno, respostas):
    total_pontos = sum(Resposta.objects.get(id=resposta_id).valor for resposta_id in respostas.values())

    if total_pontos <=2:
        aluno.espectro = 'Baixo'
    elif total_pontos <=7:
        aluno.espectro = 'Médio'
    elif total_pontos <=8:
        aluno.espectro = 'Alto'

    aluno.save()

def resultado(request):
    aluno = Aluno.objects.get(user=request.user)
    return render(request, 'resultado.html', {'aluno': aluno})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('questionario')  # Redireciona para a página de questionário após o login
            else:
                error_message = "Usuário ou senha incorretos. Por favor, tente novamente."
                return render(request, 'login.html', {'form': form, 'error_message': error_message})
        else:
            error_message = "Formulário inválido. Por favor, tente novamente."
            return render(request, 'login.html', {'form': form, 'error_message': error_message})
    else:
        form = AuthenticationForm()
    
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')


def minha_view(request):
    if request.user.is_authenticated:
        logged_in = True
    else:
        logged_in = False

    if request.method == 'POST' and 'logout' in request.POST:
        logout(request)
        return redirect('home')  # Redireciona para a página inicial após logout

    return render(request, 'minha_template.html', {'logged_in': logged_in})

def cadastro(request):
    form = CadastroForm()
    if request.method == 'POST':
        form = CadastroForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redireciona para a página de login após o cadastro

    return render(request, 'cadastro.html', {'form': form})

def home(request):
    return render(request, 'home.html')