from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    path('aluno_dashboard/', views.aluno_dashboard, name='aluno_dashboard'),
    path('professor/dashboard/', views.professor_dashboard, name='professor_dashboard'),
    path('diretor/dashboard/', views.diretor_dashboard, name='diretor_dashboard'),

    path('aluno/notas/', views.consulta_notas, name='consulta_notas'),
    path('aluno/frequencia/', views.consulta_frequencia, name='consulta_frequencia'),
    path('disciplinas/', views.listar_disciplinas_aluno, name='listar_disciplinas_aluno'),
    path('disciplinas/inscrever/<int:disciplina_id>/', views.inscrever_em_disciplina, name='inscrever_em_disciplina'),
    path('disciplinas/minhas/', views.minhas_disciplinas, name='minhas_disciplinas'),

    path('disciplinas/professor/', views.disciplinas_professor, name='disciplinas_professor'),
    path('disciplinas/professor/<int:disciplina_id>/', views.gerenciar_alunos, name='gerenciar_alunos'),
    path('professor/notas/', views.registrar_nota, name='registrar_nota'),
    path('professor/frequencia/', views.registrar_frequencia, name='registrar_frequencia'),

    path('diretor/serie/criar/', views.criar_serie, name='criar_serie'),
    path('diretor/serie/listar/', views.listar_series, name='listar_series'),
    path('diretor/turma/criar/', views.criar_turma, name='criar_turma'),
    path('diretor/turma/listar/', views.listar_turmas, name='listar_turmas'),
    path('diretor/disciplina/criar/', views.criar_disciplina, name='criar_disciplina'),
    path('diretor/disciplina/listar/', views.listar_disciplinas, name='listar_disciplinas')

]
