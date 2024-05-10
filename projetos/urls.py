from django.urls import path
from .views import cadastro, aluno, perquest, administracao, home, login_view, logout_view, teste, realizados, refazer_teste

urlpatterns = [
    path('', home, name='home'),
    path('login/', login_view, name='login_view'),
    path('logout/', logout_view, name='logout_view'),
    path('cadastro/', cadastro, name='cadastro'),
    path('aluno/', aluno, name='aluno'),
    path('perquest/', perquest, name='perquest'),
    path('administracao/', administracao, name='administracao'),
    path('teste/', teste, name='teste'),
    path('realizados', realizados, name='realizados'),
    path('refazer_teste', refazer_teste, name='refazer_teste'),
]