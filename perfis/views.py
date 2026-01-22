from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import CadastroUsuarioForm

def cadastro_view(request):
    #if request.user.is_authenticated:
        #return redirect('pos_login')
        
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
    try:
        perfil = request.user.perfil
    except AttributeError:
        if request.user.is_staff:
            return redirect('admin:index')
        return redirect('home')

    # 1️⃣ VALIDAÇÃO DE STATUS
    if perfil.status == 'PENDENTE':
        return redirect('cadastro_pendente')
    
    if perfil.status == 'REJEITADO':
        messages.error(request, "Seu acesso foi bloqueado. Contate o suporte.")
        return redirect('login')
    
    # AFILIADOS
    if perfil.tipo_usuario == 'AFILIADO':
        if hasattr(perfil, 'dados_afiliado'):
            return redirect('afiliados:meu_perfil')
        return redirect('afiliados:cadastro_afiliado')

    #  ASSOCIADOS
    if perfil.tipo_usuario == 'ASSOCIADO':
        if hasattr(perfil, 'empresa'):
            return redirect('minha_empresa')
        return redirect('empresa_cadastrar')

    if perfil.tipo_usuario == 'COLETIVO':
        return redirect('area_institucional')

    return redirect('home')

@login_required
def cadastro_pendente_view(request):
    return render(request, 'perfis/cadastro_pendente.html', {
        'nome_usuario': request.user.get_full_name() or request.user.username
    })