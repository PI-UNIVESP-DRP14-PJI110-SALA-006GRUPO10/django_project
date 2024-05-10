from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import CadastroForm, EscolaForm, AlunoForm
from django.contrib.auth.forms import AuthenticationForm
from .models import Aluno, Resposta, Resultado, Escola, Perquest, Usuario
from django import forms

def home(request):
    return render(request, 'home.html')

def cadastro(request):
    form = CadastroForm()
    if request.method == 'POST':
        form = CadastroForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login_view')

    return render(request, 'cadastro.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('realizados')
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
    return redirect('login_view')

@login_required
def perquest(request):
    resultados = None  # Inicializa resultados como None
    if request.method == 'POST':
        respostas = {}
        for key, value in request.POST.items():
            if key.startswith('perquest_'):
                pergunta_id = int(key.split('_')[1])
                resposta_id = int(value)
                respostas[pergunta_id] = resposta_id

        # Processa as respostas e determina o nível do espectro
        espectro = processar_respostas(respostas)

        # Obtém o usuário logado
        usuario = Usuario.objects.get(user=request.user)

        # Obtém o questionário mais recente do usuário
        aluno_recente = Aluno.objects.filter(usuario=usuario).order_by('-data').first()

        # Cria um novo resultado associado ao questionário e usuário
        resultado = Resultado.objects.create(cod_alu=aluno_recente, cod_usu=usuario, nivel=espectro)

        # Obtém os resultados associados ao usuário
        resultados = Resultado.objects.filter(cod_usu=usuario).order_by('-id')[:1]

    # Obtém informações do aluno
    usuario = Usuario.objects.get(user=request.user)
    aluno_recente = Aluno.objects.filter(usuario=usuario).order_by('-data').first()
    nome_questionario = aluno_recente.nome
    idade = aluno_recente.idade
    escola = aluno_recente.usuario.escola.nome if aluno_recente.usuario.escola else "Não especificada"
    data = aluno_recente.data.strftime("%d/%m/%Y")

    perquests = Perquest.objects.all()
    contexto = {
        'perquests': perquests,
        'nome_questionario': nome_questionario,
        'idade': idade,
        'escola': escola,
        'data': data,
        'resultados': resultados,
    }
    return render(request, 'perquest.html', contexto)

def processar_respostas(respostas):
    total_pontos = sum(Resposta.objects.get(id=resposta_id).valor for resposta_id in respostas.values())

    print("Total de pontos:", total_pontos)  # Adiciona este print para verificar o total de pontos

    if total_pontos <= 2:
        espectro = 'Baixo'
    elif total_pontos <= 7:
        espectro = 'Médio'
    else:
        espectro = 'Alto'

    print("Espectro:", espectro)  # Adiciona este print para verificar o espectro atribuído
    return espectro


@login_required
def aluno(request):
    if request.method == 'POST':
        form = AlunoForm(request.POST)
        if form.is_valid():
            # Verifica se já existe um usuário associado ao User
            usuario, created = Usuario.objects.get_or_create(user=request.user)

            # Se o usuário não existir, cria um novo
            if created:
                usuario.nome = request.user.username  # Define o nome do usuário como o nome de usuário do User
                usuario.save()

            aluno = form.save(usuario)  # Salva o questionário no banco de dados, passando o usuário como argumento

            return redirect('perquest')
    else:
        form = AlunoForm()
    return render(request, 'aluno.html', {'form': form})

def administracao(request):
    if request.method == 'POST':
        form = EscolaForm(request.POST)
        if form.is_valid():
            escola = form.saveEscola()
            return redirect('administracao')
    else:
        form = EscolaForm()
    return render(request, 'administracao.html', {'form': form})

class EscolaExistenteForm(forms.Form):
    escola = forms.ModelChoiceField(queryset=Escola.objects.all(), label='Escola')

def teste(request):
    espectro = None
    if request.method == 'POST':
        respostas = {}
        total_pontos = 0
        for key, value in request.POST.items():
            if key.startswith('perquest_') and value:  # Verifica se o valor não está vazio
                pergunta_id = int(key.split('_')[1])
                resposta_id = int(value)
                respostas[pergunta_id] = resposta_id
                total_pontos += Resposta.objects.get(id=resposta_id).valor

        espectro = calcular_espectro(total_pontos)

    perguntas = Perquest.objects.all()
    respostas = {pergunta.id: '' for pergunta in perguntas}
    contexto = {'perguntas': perguntas, 'respostas': respostas, 'espectro': espectro}
    return render(request, 'teste.html', contexto)

def calcular_espectro(total_pontos):
    if total_pontos <= 2:
        return 'Baixo'
    elif total_pontos <= 7:
        return 'Médio'
    else:
        return 'Alto'

def realizados(request):
    # Verifica se o usuário está autenticado
    if not request.user.is_authenticated:
        return redirect('login_view')

    # Obtém os resultados dos testes realizados pelo usuário atual
    resultados = Resultado.objects.filter(cod_usu__user=request.user).order_by('-id')[:5]

    # Renderiza o template com os resultados dos testes e um link para refazer o teste
    return render(request, 'realizados.html', {'resultados': resultados})

def refazer_teste(request):
    # Verifica se o usuário está autenticado
    if not request.user.is_authenticated:
        return redirect('login_view')

    # Redireciona para a view 'aluno' para refazer o teste
    return redirect('aluno')
