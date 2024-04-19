from django.db import models
from django.contrib.auth.models import User

from django.db import models

class Escola(models.Model):
    nome = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    endereco = models.CharField(max_length=100)

    #def __str__(self):
        #return str(self.id) 

    def __str__(self):
        return self.nome
    
class Usuario(models.Model):  
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nome = models.CharField(max_length=100)
    escola = models.ForeignKey(Escola, on_delete=models.CASCADE,null=True)

    def __str__(self):
        return self.nome   

class Perquest(models.Model):
    texto = models.TextField()

    def __str__(self):
        return self.texto

class Resposta(models.Model):
    pergunta = models.ForeignKey(Perquest, on_delete=models.CASCADE)
    texto = models.TextField()
    valor = models.IntegerField()

    def __str__(self):
        return self.texto
    
class Aluno(models.Model):
    nome = models.CharField(max_length=100) 
    idade = models.IntegerField(default = 0)
    data = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)

    def __str__(self):
        return self.nome

class Resultado(models.Model):
    ESPECTRO_CHOICES = [
        ('Alto', 'Alto'),
        ('Médio', 'Médio'),
        ('Baixo', 'Baixo'),
    ]

    nivel = models.CharField(max_length=10, choices=ESPECTRO_CHOICES, null=True)
    cod_alu = models.ForeignKey(Aluno, on_delete=models.CASCADE)
    cod_usu = models.ForeignKey(Usuario, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.cod_alu)