from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from .forms import ClienteSignUpForm, OficinaSignUpForm, ProblemaForm, OficinaPerfilForm
from .models import Problema, User, PerfilOficina

def home(request):
    if request.user.is_authenticated:
        if request.user.is_cliente:
            return redirect('dashboard_cliente')
        elif request.user.is_oficina:
            return redirect('dashboard_oficina')
    return render(request, 'home.html')

def signup_escolha(request):
    """Renderiza a tela para escolher o tipo de conta"""
    return render(request, 'registration/signup_escolha.html')

def signup_cliente(request):
    if request.method == 'POST':
        form = ClienteSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard_cliente')
    else:
        form = ClienteSignUpForm()
    return render(request, 'registration/signup.html', {'form': form, 'tipo': 'Cliente'})

def signup_oficina(request):
    if request.method == 'POST':
        user_form = OficinaSignUpForm(request.POST)
        perfil_form = OficinaPerfilForm(request.POST)
        
        if user_form.is_valid() and perfil_form.is_valid():
            with transaction.atomic():
                user = user_form.save()
                
                perfil = perfil_form.save(commit=False)
                perfil.usuario = user
                perfil.save()
                
                perfil_form.save_m2m()
                
                login(request, user)
                return redirect('dashboard_oficina')
    else:
        user_form = OficinaSignUpForm()
        perfil_form = OficinaPerfilForm()
    
    return render(request, 'registration/signup_oficina.html', {
        'user_form': user_form,
        'perfil_form': perfil_form
    })

@login_required
def dashboard_cliente(request):
    problemas = Problema.objects.filter(cliente=request.user).order_by('-data_criacao')
    if request.method == 'POST':
        # --- ALTERADO: Incluído request.FILES para upload de imagem ---
        form = ProblemaForm(request.POST, request.FILES)
        if form.is_valid():
            problema = form.save(commit=False)
            problema.cliente = request.user
            problema.save()
            return redirect('dashboard_cliente')
    else:
        form = ProblemaForm()
    return render(request, 'dashboard_cliente.html', {'problemas': problemas, 'form': form})

@login_required
def dashboard_oficina(request):
    problemas_abertos = Problema.objects.filter(status='ABERTO')
    meus_servicos = Problema.objects.filter(oficina=request.user)
    return render(request, 'dashboard_oficina.html', {
        'problemas_abertos': problemas_abertos,
        'meus_servicos': meus_servicos
    })

@login_required
def pegar_servico(request, pk):
    problema = get_object_or_404(Problema, pk=pk)
    if not problema.oficina and request.user.is_oficina:
        problema.oficina = request.user
        problema.status = 'ANDAMENTO'
        problema.save()
    return redirect('dashboard_oficina')

@login_required
def concluir_servico(request, pk):
    problema = get_object_or_404(Problema, pk=pk)
    if problema.oficina == request.user:
        problema.status = 'CONCLUIDO'
        problema.save()
    return redirect('dashboard_oficina')