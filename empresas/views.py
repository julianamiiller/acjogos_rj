from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import EmpresaForm
from .models import Empresa

# --- VIEW: CADASTRAR ---
@login_required
def empresa_cadastrar_view(request):
    perfil = request.user.perfil

    # 🔒 Segurança: só ASSOCIADO pode acessar
    if perfil.tipo_usuario != 'ASSOCIADO':
        messages.error(request, 'Acesso negado. Apenas associados podem cadastrar empresas.')
        return redirect('home')

    # 🚫 Se já tem empresa cadastrada, redireciona para visualizar
    if hasattr(perfil, 'empresa'):
        return redirect('minha_empresa')

    if request.method == 'POST':
        form = EmpresaForm(request.POST)
        if form.is_valid():
            # 🔥 Vinculando a empresa ao perfil do usuário logado
            empresa = form.save(commit=False)
            empresa.perfil = perfil  
            empresa.save()
            
            messages.success(request, 'Empresa cadastrada com sucesso!')
            return redirect('minha_empresa')
    else:
        form = EmpresaForm()

    return render(request, 'empresas/empresa_form.html', {'form': form})


# --- VIEW: VISUALIZAR ---
@login_required
def minha_empresa_view(request):
    perfil = request.user.perfil

    # Segurança: apenas ASSOCIADO acessa
    if perfil.tipo_usuario != 'ASSOCIADO':
        messages.error(request, 'Acesso negado.')
        return redirect('home')

    # Se não tem empresa, convida a cadastrar
    if not hasattr(perfil, 'empresa'):
        return redirect('empresa_cadastrar')

    empresa = perfil.empresa

    return render(request, 'empresas/minha_empresa.html', {
        'empresa': empresa
    })


# --- VIEW: EDITAR ---
@login_required
def empresa_editar_view(request):
    perfil = request.user.perfil

    # Segurança: apenas ASSOCIADO
    if perfil.tipo_usuario != 'ASSOCIADO':
        messages.error(request, 'Acesso negado.')
        return redirect('home')

    # Verifica se a empresa existe usando hasattr (mantendo seu padrão)
    if not hasattr(perfil, 'empresa'):
        messages.warning(request, 'Você ainda não possui uma empresa cadastrada.')
        return redirect('empresa_cadastrar')

    empresa = perfil.empresa

    if request.method == 'POST':
        # instance=empresa é o que faz o Django ATUALIZAR em vez de criar novo
        form = EmpresaForm(request.POST, instance=empresa)
        if form.is_valid():
            form.save()
            messages.success(request, 'Dados da empresa atualizados com sucesso!')
            return redirect('minha_empresa')
    else:
        # Carrega o formulário preenchido com os dados atuais
        form = EmpresaForm(instance=empresa)

    return render(request, 'empresas/empresa_editar.html', {
        'form': form,
        'empresa': empresa # Enviamos a empresa caso queira usar o nome dela no título
    })