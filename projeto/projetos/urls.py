from django.urls import path
from .views import cadastro, aluno, perquest, administracao, home, login_view, logout_view, resultado

urlpatterns = [
    #path('', views.home, name='home'),
    #path('login/', views.login_view, name='login'),
    #path('cadastro/', views.cadastro, name='cadastro'),
    #path('logout/', views.logout_view, name='logout'),
    #path('perquest/', views.perquest, name='perquest'),
    #path('resultado/', views.resultado, name='resultado'),
    #path('Aluno/<int:escola_id>/', views.Aluno, name='Aluno'), 
    #path('escola/', views.escola, name='escola'),

    path('', home, name='home'),
    path('login/', login_view, name='login_view'),
    path('logout/', logout_view, name='logout_view'),
    path('cadastro/', cadastro, name='cadastro'),
    path('aluno/', aluno, name='aluno'),
    path('perquest/', perquest, name='perquest'),
    path('resultado/', resultado, name='resultado'),
    path('administracao/', administracao, name='administracao'),

]