from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Coletivo
from .forms import ColetivoForm

@login_required
def cadastro_coletivo(request):
    perfil = request.user.perfil
    
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
    perfil = request.user.perfil
    coletivo = get_object_or_404(Coletivo, perfil=perfil)
    
    # Enviando ambos para evitar erro no template
    return render(request, 'coletivos/dashboard.html', {
        'coletivo': coletivo,
        'perfil': perfil
    })

@login_required
def meu_perfil_coletivo(request):
    perfil = request.user.perfil
    coletivo = get_object_or_404(Coletivo, perfil=perfil)
    
    return render(request, 'coletivos/perfil_coletivo.html', {
        'coletivo': coletivo,
        'perfil': perfil
    })

@login_required
def editar_coletivo(request):
    perfil = request.user.perfil
    coletivo = get_object_or_404(Coletivo, perfil=perfil)
    
    if request.method == 'POST':
        form = ColetivoForm(request.POST, instance=coletivo)
        if form.is_valid():
            form.save()
            messages.success(request, 'Dados atualizados com sucesso!')
            # Certifique-se que o nome da URL em redirect está correto (coletivos:perfil ou similar)
            return redirect('coletivos:meu_perfil') 
    else:
        form = ColetivoForm(instance=coletivo)
    
    # Adicionado 'perfil' para que o cabeçalho do template funcione
    return render(request, 'coletivos/editar.html', {
        'form': form, 
        'coletivo': coletivo,
        'perfil': perfil
    })