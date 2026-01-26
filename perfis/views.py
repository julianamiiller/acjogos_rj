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
        print(f"DEBUG: Tipo de usuário: {perfil.tipo_usuario} | Status: {perfil.status}")
    except Exception as e:
        print(f"DEBUG: Erro ao buscar perfil: {e}")
        if request.user.is_staff:
            return redirect('admin:index')
        return redirect('home')

  
    status_atual = perfil.status.upper()
    if status_atual == 'PENDENTE':
        return redirect('cadastro_pendente')
    
    if status_atual == 'REJEITADO':
        messages.error(request, "Seu acesso foi bloqueado.")
        return redirect('login')
    
   
    tipo = perfil.tipo_usuario.upper()

    if tipo == 'AFILIADO':
        print("DEBUG: Entrou na lógica de AFILIADO")
      
        if hasattr(perfil, 'dados_afiliado'):
            return redirect('afiliados:meu_perfil')
        return redirect('afiliados:cadastro_afiliado')

    if tipo == 'ASSOCIADO':
        if hasattr(perfil, 'empresa'):
            return redirect('minha_empresa')
        return redirect('empresa_cadastrar')

    if tipo == 'COLETIVO':
        if hasattr(perfil, 'dados_coletivo'):
            return redirect('coletivos:dashboard')
        return redirect('coletivos:cadastro')

   
    print("DEBUG: Nenhum tipo coincidiu, indo para HOME")
    return redirect('home')

@login_required
def cadastro_pendente_view(request):
    return render(request, 'perfis/cadastro_pendente.html', {
        'nome_usuario': request.user.get_full_name() or request.user.username
    })