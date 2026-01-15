from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import EmpresaForm
from .models import Empresa

@login_required
def empresa_cadastrar_view(request):
    perfil = request.user.perfil

    # 🔒 Segurança: só ASSOCIADO pode acessar
    if perfil.tipo_usuario != 'ASSOCIADO':
        messages.error(request, 'Acesso negado. Apenas associados podem cadastrar empresas.')
        return redirect('home')

    # 🚫 Se já tem empresa cadastrada, redireciona para evitar duplicidade
    if hasattr(perfil, 'empresa'):
        return redirect('minha_empresa')

    if request.method == 'POST':
        form = EmpresaForm(request.POST)
        if form.is_valid():
            # 🔥 Ponto Crítico: Salvando com vínculo ao perfil
            empresa = form.save(commit=False)
            empresa.perfil = perfil  
            empresa.save()
            
            messages.success(request, 'Empresa cadastrada com sucesso!')
            return redirect('minha_empresa')
    else:
        form = EmpresaForm()

    return render(request, 'empresas/empresa_form.html', {'form': form})


@login_required
def minha_empresa_view(request):
    perfil = request.user.perfil

    # Segurança: apenas ASSOCIADO acessa
    if perfil.tipo_usuario != 'ASSOCIADO':
        messages.error(request, 'Acesso negado.')
        return redirect('home')

    # Se não tem empresa, redireciona para o formulário de cadastro
    if not hasattr(perfil, 'empresa'):
        return redirect('empresa_cadastrar')

    empresa = perfil.empresa

    return render(request, 'empresas/minha_empresa.html', {
        'empresa': empresa
    })