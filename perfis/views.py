from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CadastroUsuarioForm
from django.contrib.auth.decorators import login_required

def cadastro_view(request):
    if request.method == 'POST':
        form = CadastroUsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cadastro realizado com sucesso! Aguarde a aprovação administrativa.')
            return redirect('login')
        else:
            # Se houver erro (como username já existente), o Django avisará no form.errors
            print(form.errors) 
    else:
        form = CadastroUsuarioForm()
    return render(request, 'registration/cadastro.html', {'form': form})

@login_required
def pos_login_view(request):
    # Pega o perfil vinculado ao usuário logado
    perfil = request.user.perfil 

    # --- 1️⃣ VALIDAÇÃO DE STATUS (NOVA ATUALIZAÇÃO) ---
    if perfil.status == 'PENDENTE':
        return redirect('cadastro_pendente')
    
    if perfil.status == 'REJEITADO':
        # Você pode criar uma página para explicar o motivo da rejeição ou apenas deslogar
        messages.error(request, "Seu cadastro foi rejeitado. Entre em contato com o suporte.")
        return redirect('login')

    # --- 2️⃣ REDIRECIONAMENTO POR TIPO DE USUÁRIO (SUA BASE) ---
    
    if perfil.tipo_usuario == 'ASSOCIADO':
        return redirect('empresa_cadastrar')

    if perfil.tipo_usuario == 'AFILIADO':
        return redirect('perfil_completar')

    if perfil.tipo_usuario == 'COLETIVO':
        return redirect('area_institucional')

    # 3️⃣ Se for DIRETOR ou qualquer outro caso aprovado
    return redirect('home')

@login_required
def cadastro_pendente_view(request):
    """
    Página que informa ao usuário que ele deve aguardar a aprovação
    antes de acessar as funcionalidades do sistema.
    """
    return render(request, 'perfis/cadastro_pendente.html', {
        'nome_usuario': request.user.username
    })