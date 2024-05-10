from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views import generic, View
from django.views.generic import TemplateView, DetailView, UpdateView, DeleteView
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from .forms import CustomUserCreationForm, StudentForm
from .models import Question, Response, UserProfile, School, Role, Student
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    redirect_authenticated_user = True
    next_page = reverse_lazy('home')

    def form_invalid(self, form):
        messages.error(self.request, "FALHA NO LOGIN")
        return render(self.request, self.template_name, {'form': form})


class InitialPageView(LoginView):
    template_name = 'mchatr/initial_page.html'
    redirect_authenticated_user = True
    success_url = reverse_lazy('mchatr:success_page')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class SignUpView(generic.CreateView):
    form_class = CustomUserCreationForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['schools'] = School.objects.all()
        context['roles'] = Role.objects.all()
        return context


class HomeView(TemplateView):
    template_name = 'mchatr/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['students'] = Student.objects.filter(creator=self.request.user)
        return context


class LoggedQuizView(LoginRequiredMixin, View):
    template_name = 'mchatr/logged_quiz.html'

    def get(self, request, student_id):
        student = get_object_or_404(Student, pk=student_id, creator=request.user)
        questions = Question.objects.all()
        return render(request, self.template_name, {'questions': questions, 'student': student})

    def post(self, request, student_id):
        student = get_object_or_404(Student, pk=student_id, creator=request.user)
        score = 0
        questions = Question.objects.all()
        for index, question in enumerate(questions, start=1):
            response = request.POST.get(f'q{index}', 'No')
            if (response == 'Yes' and question.id in [11, 18, 20, 22]) or (response == 'No' and question.id not in [11, 18, 20, 22]):
                score += 1
        student.mchatr_score = score
        student.save()
        return redirect('student_detail', pk=student.pk)


# class LoggedResultView(View):
#     def get(self, request, *args, **kwargs):
#         responses = Response.objects.all()
#         score = sum(1 for response in responses if (response.answer and response.question.id in [2, 5, 12]) or (not response.answer and response.question.id not in [2, 5, 12]))
#         risk_level = 'BAIXO' if score < 3 else 'MÉDIO' if score < 5 else 'ALTO'
#         return render(request, 'mchatr/result.html', {'risk_level': risk_level})

class LoggedResultView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        student = get_object_or_404(Student, pk=kwargs['pk'], creator=request.user)
        # Assuming you have a method to calculate the risk level based on the student's score
        risk_level = 'BAIXO' if score < 3 else 'MÉDIO' if score < 5 else 'ALTO'
        return render(request, 'mchatr/result.html', {'risk_level': risk_level})


class IdempoQuizView(View):
    def get(self, request, *args, **kwargs):
        questions = Question.objects.all()
        return render(request, 'mchatr/idempo_quiz.html', {'questions': questions})

    def post(self, request, *args, **kwargs):
        score = 0
        questions = Question.objects.all()
        for index, question in enumerate(questions, start=1):
            response = request.POST.get(f'q{index}', 'No')
            if (response == 'Yes' and question.id in [11, 18, 20, 22]) or (response == 'No' and question.id not in [11, 18, 20, 22]):
                score += 1
        risk_level = 'BAIXO' if score < 3 else 'MÉDIO' if score < 5 else 'ALTO'
        return render(request, 'mchatr/result.html', {'risk_level': risk_level})


class CreateView(generic.CreateView):
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['schools'] = School.objects.all()
        context['roles'] = Role.objects.all()
        return context
    

class StudentCreateView(CreateView):
    model = Student
    form_class = StudentForm
    template_name = 'mchatr/create_student.html'
    success_url = reverse_lazy('home')
    
    def form_valid(self, form):
        student_count = Student.objects.filter(creator=self.request.user).count()
        if student_count >= 100:
            messages.error(self.request, "You cannot create more than 100 students.")
            return self.form_invalid(form)
        form.instance.creator = self.request.user
        return super().form_valid(form)


class StudentDetailView(LoginRequiredMixin, View):
    template_name = 'mchatr/read_student.html'

    def get(self, request, pk):
        student = get_object_or_404(Student, pk=pk, creator=request.user)
        context = {
            'student': student,
            'risk_level': None if student.mchatr_score is None else ('BAIXO' if student.mchatr_score < 3 else 'MÉDIO' if student.mchatr_score < 5 else 'ALTO')
        }
        return render(request, self.template_name, context)
    

class StudentUpdateView(LoginRequiredMixin, UpdateView):
    model = Student
    form_class = StudentForm
    template_name = 'mchatr/update_student.html'
    success_url = reverse_lazy('home')  # Redirect to the home page after a successful update

    def get_object(self, queryset=None):
        """Hook to ensure object is retrieved only if the logged-in user is the creator."""
        # Ensure the default queryset is filtered by creator
        if queryset is None:
            queryset = self.get_queryset()
        # pk is fetched from URL conf
        pk = self.kwargs.get(self.pk_url_kwarg)
        return get_object_or_404(queryset, pk=pk, creator=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Atualizar Aluno'
        return context


class StudentDeleteView(LoginRequiredMixin, DeleteView):
    model = Student
    success_url = reverse_lazy('home')  # Redirect to the home page after deletion

    def get_object(self, queryset=None):
        queryset = self.model.objects.filter(creator=self.request.user)
        # Get the primary key from URL kwargs
        pk = self.kwargs.get('pk')
        return get_object_or_404(queryset, pk=pk)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return HttpResponseRedirect(self.get_success_url())