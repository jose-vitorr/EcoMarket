from django.contrib.auth.models import AbstractUser, User
from django.db import models

class User(AbstractUser):
    
    USER_TYPES = [
        ('ALUNO', 'Aluno'),
        ('PROFESSOR', 'Professor'),
        ('DIRETOR', 'Diretor'),
    ]

    user_type = models.CharField(max_length=10, choices=USER_TYPES, default='ALUNO')

    def __str__(self):
        return f"{self.username} ({self.get_user_type_display()})"

class Serie(models.Model):
    nome = models.CharField(max_length=50)

    def __str__(self):
        return self.nome

class Turma(models.Model):
    nome = models.CharField(max_length=10)  
    serie = models.ForeignKey(Serie, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.serie.nome} - {self.nome}"

class Disciplina(models.Model):
    nome = models.CharField(max_length=100)
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE)
    professor = models.ForeignKey(User, on_delete=models.CASCADE)  

    def __str__(self):
        return f"{self.nome} ({self.turma.nome})"

class Inscricao(models.Model):
    aluno = models.ForeignKey(User, on_delete=models.CASCADE)  
    disciplina = models.ForeignKey(Disciplina, on_delete=models.CASCADE)
    faltas = models.IntegerField(default=0)
    frequencia = models.FloatField(default=0.0)  
    nota = models.FloatField(default=0.0)

    def __str__(self):
        return f"{self.aluno.username} - {self.disciplina.nome}"
    
class Nota(models.Model):
    aluno = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'user_type': 'ALUNO'})
    disciplina = models.ForeignKey(Disciplina, on_delete=models.CASCADE)
    nota = models.FloatField()
    data_lancamento = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.aluno.username} - {self.disciplina.nome} - {self.nota}"
    
class Frequencia(models.Model):
    aluno = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'user_type': 'ALUNO'})
    disciplina = models.ForeignKey(Disciplina, on_delete=models.CASCADE)
    presente = models.BooleanField()
    data = models.DateField()

    def __str__(self):
        return f"{self.aluno.username} - {self.disciplina.nome} - {'Presente' if self.presente else 'Ausente'}"