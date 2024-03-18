from django.db import models
from django.contrib.auth.models import User

from django.db import models

class Aluno(models.Model):
    ESPECTRO_CHOICES = [
        ('Alto', 'Alto'),
        ('Médio', 'Médio'),
        ('Baixo', 'Baixo'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nome = models.CharField(max_length=100)
    cpf_rg = models.CharField(max_length=20)
    idade = models.IntegerField(null=True, blank=True)
    endereco = models.CharField(max_length=200)
    nome_responsavel = models.CharField(max_length=100)
    espectro = models.CharField(max_length=10, choices=ESPECTRO_CHOICES)

    def __str__(self):
        return self.nome

class Pergunta(models.Model):
    texto = models.TextField()

    def __str__(self):
        return self.texto

class Resposta(models.Model):
    pergunta = models.ForeignKey(Pergunta, on_delete=models.CASCADE)
    texto = models.TextField()
    valor = models.IntegerField()

    def __str__(self):
        return self.texto