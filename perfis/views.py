from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import CadastroUsuarioForm
from django.contrib.auth.decorators import login_required

# 1. VIEW DE CADASTRO (Mantida com pequenas melhorias de fluxo)
def cadastro_view(request):
    if request.method == 'POST':
        form = CadastroUsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cadastro realizado com sucesso! Aguarde a aprovação administrativa.')
            return redirect('login')
        else:
            # Mantendo seu print para debug, mas os erros já aparecem no template via form.errors
            print(form.errors) 
    else:
        form = CadastroUsuarioForm()
    return render(request, 'registration/cadastro.html', {'form': form})

# 2. VIEW POS-LOGIN (A "Central de Inteligência" do seu redirecionamento)
@login_required
def pos_login_view(request):
    # Tenta pegar o perfil. Se não existir, você pode redirecionar para criar um       #AFILIADO → meu_perfil

    try:
        perfil = request.user.perfil
    except AttributeError:
        # Caso o usuário seja admin ou não tenha perfil criado ainda
        if request.user.is_staff:
            return redirect('admin:index')
        return redirect('home')

    # --- 1️⃣ VALIDAÇÃO DE STATUS ---
    if perfil.status == 'PENDENTE':
        return redirect('cadastro_pendente')
    
    if perfil.status == 'REJEITADO':
        messages.error(request, "Seu cadastro foi rejeitado. Entre em contato com o suporte.")
        # É importante deslogar o usuário aqui se o login for automático
        return redirect('login')

    # --- 2️⃣ REDIRECIONAMENTO POR TIPO DE USUÁRIO ---
    
    if perfil.tipo_usuario == 'ASSOCIADO':
        # Verificação robusta: Checa se existe uma empresa vinculada a este perfil
        # Nota: Certifique-se que no seu model Empresa exista um OneToOneField ou ForeignKey para Perfil ou User
        if hasattr(perfil, 'empresa') and perfil.empresa:
            return redirect('minha_empresa')
        else:
            return redirect('empresa_cadastrar')

    if perfil.tipo_usuario == 'AFILIADO':
        return redirect('perfil_completar')

    if perfil.tipo_usuario == 'COLETIVO':
        return redirect('area_institucional')

    # 3️⃣ Caso padrão (DIRETOR ou outros aprovados)
    return redirect('home')

# 3. VIEW DE STATUS PENDENTE
@login_required
def cadastro_pendente_view(request):
    return render(request, 'perfis/cadastro_pendente.html', {
        'nome_usuario': request.user.username
    })

#meu_perfil_view

#perfil_editar_view

#ESSAS VIEWS PRECISAM EXISTIR PARA O AFILIADO