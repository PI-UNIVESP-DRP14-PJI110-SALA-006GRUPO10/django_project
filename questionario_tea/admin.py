from django.contrib import admin
from .models import Aluno, Pergunta, Resposta

class RespostaInline(admin.StackedInline):
    model = Resposta
    extra = 1

@admin.register(Pergunta)
class PerguntaAdmin(admin.ModelAdmin):
    inlines = [RespostaInline]

admin.site.register(Aluno)