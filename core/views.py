from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.shortcuts import render, redirect, get_object_or_404
from .models import Serie, Turma, Disciplina, User, Inscricao, Nota, Frequencia
from .forms import CustomLoginForm, SerieForm
from django.http import HttpResponseForbidden

def login_view(request):
    if request.method == 'POST':
        form = CustomLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            
            if user.user_type == 'ALUNO':
                return redirect('aluno_dashboard')
            elif user.user_type == 'PROFESSOR':
                return redirect('professor_dashboard')
            elif user.user_type == 'DIRETOR':
                return redirect('diretor_dashboard')
    else:
        form = CustomLoginForm()
    return render(request, 'core/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def diretor_dashboard(request):
    if request.user.user_type != 'DIRETOR':
        return HttpResponseForbidden("Apenas diretores podem acessar esta página.")
    return render(request, 'core/diretor_dashboard.html')

@login_required
def professor_dashboard(request):
    if request.user.user_type != 'PROFESSOR':
        return HttpResponseForbidden("Apenas professores podem acessar esta página.")
    return render(request, 'core/professor_dashboard.html')

@login_required
def aluno_dashboard(request):
    if request.user.user_type != 'ALUNO':
        return HttpResponseForbidden("Apenas alunos podem acessar esta página.")
    return render(request, 'core/aluno_dashboard.html')

@login_required
def criar_serie(request):
    if request.user.user_type != 'DIRETOR':
        return HttpResponseForbidden("Apenas diretores podem acessar esta página.")

    if request.method == 'POST':
        form = SerieForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_series')
    else:
        form = SerieForm()

    return render(request, 'core/criar_serie.html', {'form': form})

@login_required
def listar_series(request):
    if request.user.user_type != 'DIRETOR':
        return HttpResponseForbidden("Apenas diretores podem acessar esta página.")

    series = Serie.objects.all()
    return render(request, 'core/listar_series.html', {'series': series})

@login_required
def criar_turma(request):
    if request.user.user_type != 'DIRETOR':
        return HttpResponseForbidden("Apenas diretores podem acessar esta página.")

    if request.method == 'POST':
        nome = request.POST.get('nome')
        serie_id = request.POST.get('serie')
        serie = Serie.objects.get(id=serie_id)
        Turma.objects.create(nome=nome, serie=serie)
        return redirect('listar_turmas')
    else:
        series = Serie.objects.all()
    return render(request, 'core/criar_turma.html', {'series': series})

@login_required
def criar_disciplina(request):
    if request.user.user_type != 'DIRETOR':
        return HttpResponseForbidden("Apenas diretores podem acessar esta página.")

    if request.method == 'POST':
        nome = request.POST.get('nome')
        turma_id = request.POST.get('turma')
        professor_id = request.POST.get('professor')
        turma = Turma.objects.get(id=turma_id)
        professor = User.objects.get(id=professor_id)
        Disciplina.objects.create(nome=nome, turma=turma, professor=professor)
        return redirect('listar_disciplinas')
    else:
        turmas = Turma.objects.all()
        professores = User.objects.filter(user_type='PROFESSOR')
    return render(request, 'core/criar_disciplina.html', {'turmas': turmas, 'professores': professores})

@login_required
def listar_disciplinas(request):
    if request.user.user_type != 'DIRETOR':
        return HttpResponseForbidden("Apenas diretores podem acessar esta página.")

    disciplinas = Disciplina.objects.select_related('turma', 'professor').all()
    return render(request, 'core/listar_disciplinas.html', {'disciplinas': disciplinas})

@login_required
def listar_turmas(request):
    if request.user.user_type != 'DIRETOR':
        return HttpResponseForbidden("Apenas diretores podem acessar esta página.")

    turmas = Turma.objects.select_related('serie').all()  
    return render(request, 'core/listar_turmas.html', {'turmas': turmas})

@login_required
def listar_disciplinas_aluno(request):
    if request.user.user_type != 'ALUNO':
        return HttpResponseForbidden("Apenas alunos podem acessar esta página.")

    disciplinas = Disciplina.objects.exclude(inscricao__aluno=request.user)
    return render(request, 'core/disciplinas_aluno.html', {'disciplinas': disciplinas})

@login_required
def inscrever_em_disciplina(request, disciplina_id):
    if request.user.user_type != 'ALUNO':
        return HttpResponseForbidden("Apenas alunos podem acessar esta página.")

    disciplina = get_object_or_404(Disciplina, id=disciplina_id)
    Inscricao.objects.create(aluno=request.user, disciplina=disciplina)
    return redirect('listar_disciplinas_aluno')

@login_required
def minhas_disciplinas(request):
    if request.user.user_type != 'ALUNO':
        return HttpResponseForbidden("Apenas alunos podem acessar esta página.")

    inscricoes = Inscricao.objects.filter(aluno=request.user)
    return render(request, 'core/minhas_disciplinas.html', {'inscricoes': inscricoes})

@login_required
def disciplinas_professor(request):
    if request.user.user_type != 'PROFESSOR':
        return HttpResponseForbidden("Apenas professores podem acessar esta página.")

    disciplinas = Disciplina.objects.filter(professor=request.user)
    return render(request, 'core/disciplinas_professor.html', {'disciplinas': disciplinas})

@login_required
def gerenciar_alunos(request, disciplina_id):
    if request.user.user_type != 'PROFESSOR':
        return HttpResponseForbidden("Apenas professores podem acessar esta página.")

    disciplina = get_object_or_404(Disciplina, id=disciplina_id, professor=request.user)
    alunos = Inscricao.objects.filter(disciplina=disciplina)

    if request.method == 'POST':
        for inscricao in alunos:
            inscricao.faltas = request.POST.get(f"faltas_{inscricao.id}", inscricao.faltas)
            inscricao.nota = request.POST.get(f"nota_{inscricao.id}", inscricao.nota)
            inscricao.save()
        return redirect('disciplinas_professor')

    return render(request, 'core/gerenciar_alunos.html', {'disciplina': disciplina, 'alunos': alunos})

@login_required
def consulta_notas(request):
    if request.user.user_type != 'ALUNO':
        return HttpResponseForbidden("Apenas alunos podem acessar esta página.")
    
    notas = Nota.objects.filter(aluno=request.user).select_related('disciplina')
    return render(request, 'core/consulta_notas.html', {'notas': notas})

@login_required
def consulta_frequencia(request):
    if request.user.user_type != 'ALUNO':
        return HttpResponseForbidden("Apenas alunos podem acessar esta página.")
    
    frequencias = Frequencia.objects.filter(aluno=request.user).select_related('disciplina')
    return render(request, 'core/consulta_frequencia.html', {'frequencias': frequencias})

@login_required
def registrar_nota(request):
    if request.user.user_type != 'PROFESSOR':
        return HttpResponseForbidden("Apenas professores podem acessar esta página.")
    
    if request.method == 'POST':
        aluno_id = request.POST.get('aluno')
        disciplina_id = request.POST.get('disciplina')
        nota = request.POST.get('nota')
        aluno = User.objects.get(id=aluno_id)
        disciplina = Disciplina.objects.get(id=disciplina_id, professor=request.user)
        Nota.objects.create(aluno=aluno, disciplina=disciplina, nota=nota)
        return redirect('registrar_nota')
    
    disciplinas = Disciplina.objects.filter(professor=request.user)
    alunos = User.objects.filter(user_type='ALUNO')
    return render(request, 'core/registrar_nota.html', {'disciplinas': disciplinas, 'alunos': alunos})

@login_required
def registrar_frequencia(request):
    if request.user.user_type != 'PROFESSOR':
        return HttpResponseForbidden("Apenas professores podem acessar esta página.")
    
    if request.method == 'POST':
        aluno_id = request.POST.get('aluno')
        disciplina_id = request.POST.get('disciplina')
        presente = request.POST.get('presente') == 'on'
        aluno = User.objects.get(id=aluno_id)
        disciplina = Disciplina.objects.get(id=disciplina_id, professor=request.user)
        Frequencia.objects.create(aluno=aluno, disciplina=disciplina, presente=presente, data=request.POST.get('data'))
        return redirect('registrar_frequencia')
    
    disciplinas = Disciplina.objects.filter(professor=request.user)
    alunos = User.objects.filter(user_type='ALUNO')
    return render(request, 'core/registrar_frequencia.html', {'disciplinas': disciplinas, 'alunos': alunos})
