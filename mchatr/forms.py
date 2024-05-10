from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile, School, Role, Student, Turma


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['nome', 'turma', 'escola']
        
    def __init__(self, *args, **kwargs):
        super(StudentForm, self).__init__(*args, **kwargs)
        self.fields['turma'].queryset = Turma.objects.all()
        self.fields['escola'].queryset = School.objects.all()


class CustomUserCreationForm(UserCreationForm):
    school = forms.ModelChoiceField(queryset=School.objects.all(), empty_label="Selecione uma escola", required=True)
    role = forms.ModelChoiceField(queryset=Role.objects.all(), empty_label="Selecione uma função", required=True)

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'school', 'role')

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            UserProfile.objects.create(user=user, school=self.cleaned_data['school'], role=self.cleaned_data['role'])
        return user

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].widget.attrs.update({'class': 'form-control'})