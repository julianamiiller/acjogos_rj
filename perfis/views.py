from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import CadastroUsuarioForm

def cadastro_view(request):
    
    if request.method == 'POST':
        form = CadastroUsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cadastro realizado com sucesso! Aguarde a aprovação.')
            return redirect('login')
    else:
        form = CadastroUsuarioForm()
    return render(request, 'registration/cadastro.html', {'form': form})

@login_required
def pos_login_view(request):
    print(f"DEBUG: Usuário {request.user.username} logou.")
    
    try:
        perfil = request.user.perfil
        tipo = perfil.tipo_usuario.upper()
        status_atual = perfil.status.upper()
        print(f"DEBUG: Tipo de usuário: {tipo} | Status: {status_atual}")
    except Exception as e:
        print(f"DEBUG: Erro ao buscar perfil: {e}")
        if request.user.is_staff:
            return redirect('admin:index')
        return redirect('home')

    # 1. Bloqueio de Rejeitados
    if status_atual == 'REJEITADO':
        messages.error(request, "Seu acesso foi bloqueado.")
        return redirect('login')
    
    # 2. Garantir Cadastro de Dados Específicos (Mesmo se PENDENTE)
    if tipo == 'AFILIADO':
        if not hasattr(perfil, 'dados_afiliado'):
            return redirect('afiliados:cadastro_afiliado')

    elif tipo == 'ASSOCIADO':
        if not hasattr(perfil, 'empresa'):
            return redirect('empresa_cadastrar')

    elif tipo == 'COLETIVO':
        if not hasattr(perfil, 'dados_coletivo'):
            return redirect('coletivos:cadastro')

    # 3. Se cadastro completo, checa se está PENDENTE
    if status_atual == 'PENDENTE':
        return redirect('cadastro_pendente')
    
    # 4. Redirecionamentos para Usuários APROVADOS
    if tipo == 'AFILIADO':
        return redirect('core_dashboard:dashboard')

    if tipo == 'ASSOCIADO':
        return redirect('minha_empresa')

    if tipo == 'COLETIVO':
        return redirect('coletivos:dashboard')

    if tipo == 'DIRETOR':
        return redirect('core_dashboard:dashboard')

    return redirect('home')

@login_required
def cadastro_pendente_view(request):
    return render(request, 'perfis/cadastro_pendente.html', {
        'nome_usuario': request.user.get_full_name() or request.user.username
    })