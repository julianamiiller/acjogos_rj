from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Coletivo
from .forms import ColetivoForm

@login_required
def cadastro_coletivo(request):
    try:
        perfil = request.user.perfil
    except request.user._meta.model.perfil.RelatedObjectDoesNotExist:
        messages.error(request, 'Perfil de usuário não encontrado.')
        return redirect('home')
    
    if perfil.tipo_usuario != 'COLETIVO':
        messages.error(request, 'Acesso negado.')
        return redirect('home')
    
    if hasattr(perfil, 'dados_coletivo'):
        return redirect('coletivos:dashboard')

    if request.method == 'POST':
        form = ColetivoForm(request.POST)
        if form.is_valid():
            coletivo = form.save(commit=False)
            coletivo.perfil = perfil
            coletivo.save()
            messages.success(request, 'Cadastro realizado com sucesso!')
            return redirect('coletivos:dashboard')
    else:
        form = ColetivoForm()
    
    # Adicionado 'perfil' ao contexto
    return render(request, 'coletivos/cadastro_coletivo.html', {
        'form': form, 
        'perfil': perfil
    })

@login_required
def dashboard_coletivo(request):
    return redirect('core_dashboard:dashboard')

@login_required
def meu_perfil_coletivo(request):
    try:
        perfil = request.user.perfil
    except request.user._meta.model.perfil.RelatedObjectDoesNotExist:
        messages.error(request, 'Perfil de usuário não encontrado.')
        return redirect('home')

    if perfil.tipo_usuario != 'COLETIVO':
        messages.error(request, 'Acesso restrito a instituições.')
        return redirect('core_dashboard:dashboard')

    if not hasattr(perfil, 'dados_coletivo'):
        messages.info(request, 'Por favor, complete seu cadastro institucional primeiro.')
        return redirect('coletivos:cadastro')

    coletivo = perfil.dados_coletivo
    
    return render(request, 'coletivos/perfil_coletivo.html', {
        'coletivo': coletivo,
        'perfil': perfil
    })

@login_required
def editar_coletivo(request):
    try:
        perfil = request.user.perfil
    except request.user._meta.model.perfil.RelatedObjectDoesNotExist:
        messages.error(request, 'Perfil de usuário não encontrado.')
        return redirect('home')

    if perfil.tipo_usuario != 'COLETIVO':
        messages.error(request, 'Acesso restrito a instituições.')
        return redirect('core_dashboard:dashboard')

    if not hasattr(perfil, 'dados_coletivo'):
        messages.info(request, 'Por favor, complete seu cadastro institucional primeiro.')
        return redirect('coletivos:cadastro')

    coletivo = perfil.dados_coletivo
    
    if request.method == 'POST':
        form = ColetivoForm(request.POST, instance=coletivo)
        if form.is_valid():
            form.save()
            messages.success(request, 'Dados atualizados com sucesso!')
            return redirect('coletivos:meu_perfil') 
    else:
        form = ColetivoForm(instance=coletivo)
    
    return render(request, 'coletivos/editar.html', {
        'form': form, 
        'coletivo': coletivo,
        'perfil': perfil
    })