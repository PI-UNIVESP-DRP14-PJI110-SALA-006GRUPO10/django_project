from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import InitialPageView, SignUpView, CustomLoginView, HomeView, LoggedQuizView, LoggedResultView, IdempoQuizView, StudentCreateView, StudentDetailView, StudentUpdateView, StudentDeleteView

urlpatterns = [
    path('', InitialPageView.as_view(), name='initial'),
	path('signup/', SignUpView.as_view(), name='signup'),
	path('login/', CustomLoginView.as_view(), name='login'),
	path('logout/', LogoutView.as_view(), name='logout'),
	path('home/', HomeView.as_view(), name='home'),
	path('idempo/', IdempoQuizView.as_view(), name='idempo'),
    path('result/', LoggedResultView.as_view(), name='result'),
	path('create/', StudentCreateView.as_view(), name='create_student'),
	path('quiz/<int:student_id>/', LoggedQuizView.as_view(), name='logged_quiz'),
    path('student/<int:pk>/', StudentDetailView.as_view(), name='student_detail'),
	path('update/<int:pk>/', StudentUpdateView.as_view(), name='update_student'),
	path('delete/<int:pk>/', StudentDeleteView.as_view(), name='delete_student'),
]