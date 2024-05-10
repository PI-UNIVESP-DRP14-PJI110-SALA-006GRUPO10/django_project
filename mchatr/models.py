from django.db import models
from django.contrib.auth.models import User


class Question(models.Model):
    text = models.CharField(max_length=1024)
    def __str__(self):
        return self.text


class Response(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.BooleanField()  # True for Yes, False for No


class Role(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Turma(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class School(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    email = models.EmailField(max_length=70, blank=True, unique=True)

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username + "'s profile"
    

class Student(models.Model):
    nome = models.CharField(max_length=100)
    turma = models.ForeignKey('Turma', on_delete=models.CASCADE)
    escola = models.ForeignKey(School, on_delete=models.CASCADE)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="students")
    mchatr_score = models.IntegerField(null=True, blank=True, default=None)